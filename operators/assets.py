import bpy
from ..utils import async_call, get_client
from ..api.client import SomataError

# Module-level session cache — list of asset dicts from the API.
# Not persisted across Blender restarts; refresh on demand.
_assets_cache: list = []


def get_cache() -> list:
    return _assets_cache


class SomataRefreshAssets(bpy.types.Operator):
    """Fetch the latest asset list from Somata."""

    bl_idname = "somata.refresh_assets"
    bl_label = "Refresh Assets"
    bl_description = "Reload your asset library from Somata"

    def execute(self, context):
        client = get_client()

        def do_fetch():
            return client.list_assets(limit=50)

        def on_done(result):
            global _assets_cache
            _assets_cache = result.get("assets", result) if isinstance(result, dict) else result
            # Redraw the N-panel to show the updated list
            for area in context.screen.areas:
                if area.type == "VIEW_3D":
                    area.tag_redraw()
            self.report({"INFO"}, f"Loaded {len(_assets_cache)} assets.")

        def on_error(err):
            msg = err.message if isinstance(err, SomataError) else str(err)
            self.report({"ERROR"}, f"Refresh failed: {msg}")

        async_call(do_fetch, on_done=on_done, on_error=on_error)
        return {"FINISHED"}
