import bpy
import os
import tempfile
import urllib.request
from bpy.props import StringProperty
from ..utils import async_call, get_client
from ..api.client import SomataError


class SomataDownloadMesh(bpy.types.Operator):
    """Download a READY asset's FBX and import it into the current scene."""

    bl_idname = "somata.download_mesh"
    bl_label = "Import Mesh"
    bl_description = "Download the FBX mesh and import it into the current scene"

    asset_id: StringProperty()

    def execute(self, context):
        client = get_client()
        asset_id = self.asset_id

        def do_download():
            url = client.download_url(asset_id)
            # Download to a temp file — Blender's FBX importer needs a filepath
            tmp = tempfile.NamedTemporaryFile(suffix=".fbx", delete=False)
            urllib.request.urlretrieve(url, tmp.name)
            return tmp.name

        def on_done(fbx_path):
            bpy.ops.import_scene.fbx(filepath=fbx_path)
            os.unlink(fbx_path)
            self.report({"INFO"}, "Mesh imported successfully.")

        def on_error(err):
            msg = err.message if isinstance(err, SomataError) else str(err)
            self.report({"ERROR"}, f"Download failed: {msg}")

        self.report({"INFO"}, "Downloading mesh…")
        async_call(do_download, on_done=on_done, on_error=on_error)
        return {"FINISHED"}
