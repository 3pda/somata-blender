import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper
from ..utils import async_call, get_client
from ..api.client import SomataError


class SomataUploadPhoto(bpy.types.Operator, ImportHelper):
    """Upload a reference photo to generate a photorealistic 3D mesh."""

    bl_idname = "somata.upload_photo"
    bl_label = "Pick Photo…"
    bl_description = "Open file browser to select a JPEG/PNG reference photo"

    filter_glob: StringProperty(default="*.jpg;*.jpeg;*.png;*.webp", options={"HIDDEN"})

    # These are pre-populated from scene props in invoke() so the
    # user's inputs in the panel carry into the file browser.
    asset_name: StringProperty(name="Name")
    height: FloatProperty(name="Height (cm)", default=170.0, min=100.0, max=250.0)
    weight: FloatProperty(name="Weight (kg)", default=65.0, min=30.0, max=200.0)
    gender: EnumProperty(
        name="Gender",
        items=[("male", "Male", ""), ("female", "Female", "")],
        default="female",
    )

    def invoke(self, context, event):
        # Copy current panel values into operator props before opening file browser
        self.asset_name = context.scene.somata_upload_name
        self.height = context.scene.somata_upload_height
        self.weight = context.scene.somata_upload_weight
        self.gender = context.scene.somata_upload_gender
        return ImportHelper.invoke(self, context, event)

    def draw(self, context):
        # Shown in the file browser sidebar — mirrors the panel for confirmation
        layout = self.layout
        layout.prop(self, "asset_name")
        layout.prop(self, "gender")
        layout.prop(self, "height")
        layout.prop(self, "weight")

    def execute(self, context):
        client = get_client()
        image_path = self.filepath
        name = self.asset_name or bpy.path.basename(image_path).rsplit(".", 1)[0]

        # Write back to scene so the panel reflects the last-used values
        context.scene.somata_upload_name = name
        context.scene.somata_upload_height = self.height
        context.scene.somata_upload_weight = self.weight
        context.scene.somata_upload_gender = self.gender

        def do_upload():
            return client.upload_photo(
                name=name,
                image_path=image_path,
                height=self.height,
                weight=self.weight,
                gender=self.gender,
            )

        def on_done(asset):
            self.report({"INFO"}, f"Asset '{asset['name']}' created — mesh generating in background.")

        def on_error(err):
            msg = err.message if isinstance(err, SomataError) else str(err)
            self.report({"ERROR"}, f"Upload failed: {msg}")

        self.report({"INFO"}, "Uploading…")
        async_call(do_upload, on_done=on_done, on_error=on_error)
        return {"FINISHED"}
