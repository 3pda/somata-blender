"""
Somata REST client using only Python stdlib (urllib) — no pip deps required.
All methods are synchronous. Operators call them from background threads
via somata_blender.utils.async_call to avoid blocking Blender's UI.
"""

import json
import urllib.request
import urllib.parse
import uuid
from pathlib import Path


class SomataError(Exception):
    """Raised when the API returns a non-2xx response."""
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


class SomataClient:
    def __init__(self, base_url: str, token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.token = token

    # ── Auth ─────────────────────────────────────────────────────────────────

    def login(self, email: str, password: str) -> dict:
        """Returns { token, user }."""
        return self._post("/api/auth/login", {"email": email, "password": password}, auth=False)

    def me(self) -> dict:
        return self._get("/api/auth/me")

    # ── Subscription ─────────────────────────────────────────────────────────

    def subscription(self) -> dict:
        """Returns { tier, creditsRemaining }."""
        return self._get("/api/stripe/subscription")

    # ── Assets ───────────────────────────────────────────────────────────────

    def list_assets(self, limit: int = 50, offset: int = 0) -> dict:
        return self._get(f"/api/assets/?limit={limit}&offset={offset}")

    def get_asset(self, asset_id: str) -> dict:
        return self._get(f"/api/assets/{asset_id}")

    def upload_photo(self, name: str, image_path: str, height: float, weight: float, gender: str) -> dict:
        """Upload a reference photo. Returns asset dict."""
        return self._multipart_post("/api/assets/", {
            "name": name,
            "height": str(height),
            "weight": str(weight),
            "gender": gender,
        }, file_field="image", file_path=image_path)

    def preview_body(self, gender: str, height_cm: float, weight_kg: float) -> dict:
        """Generate a free A-pose preview. Returns { previewUrl, previewToken }."""
        return self._post("/api/assets/preview-body", {
            "gender": gender,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
        })

    def generate_body(self, preview_token: str, name: str, gender: str, height_cm: float, weight_kg: float) -> dict:
        """Confirm a preview — deducts 1 credit. Returns asset dict."""
        return self._post("/api/assets/generate-body", {
            "previewToken": preview_token,
            "name": name,
            "gender": gender,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
        })

    def download_url(self, asset_id: str) -> str:
        """Returns a signed download URL for the FBX mesh."""
        data = self._post(f"/api/assets/{asset_id}/download", {})
        return data["url"]

    # ── Internal ─────────────────────────────────────────────────────────────

    def _headers(self, auth: bool = True, content_type: str = "application/json") -> dict:
        h = {"Content-Type": content_type, "Accept": "application/json"}
        if auth and self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _get(self, path: str) -> dict:
        req = urllib.request.Request(
            self.base_url + path,
            headers=self._headers(),
        )
        return self._send(req)

    def _post(self, path: str, body: dict, auth: bool = True) -> dict:
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            self.base_url + path,
            data=data,
            headers=self._headers(auth=auth),
            method="POST",
        )
        return self._send(req)

    def _multipart_post(self, path: str, fields: dict, file_field: str, file_path: str) -> dict:
        boundary = uuid.uuid4().hex
        body_parts = []

        for key, value in fields.items():
            body_parts.append(
                f'--{boundary}\r\n'
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
                f'{value}\r\n'
            )

        file_data = Path(file_path).read_bytes()
        filename = Path(file_path).name
        body_parts.append(
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'
            f'Content-Type: application/octet-stream\r\n\r\n'
        )
        body = "".join(body_parts).encode() + file_data + f'\r\n--{boundary}--\r\n'.encode()

        headers = self._headers(content_type=f"multipart/form-data; boundary={boundary}")
        req = urllib.request.Request(
            self.base_url + path,
            data=body,
            headers=headers,
            method="POST",
        )
        return self._send(req)

    def _send(self, req: urllib.request.Request) -> dict:
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            try:
                msg = json.loads(e.read()).get("error", e.reason)
            except Exception:
                msg = e.reason
            raise SomataError(e.code, msg) from e
