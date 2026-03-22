import bpy
from bpy.props import FloatProperty, EnumProperty, StringProperty
from ..utils import async_call, get_client
from ..api.client import SomataError


class SomataPreviewBody(bpy.types.Operator):
    """Generate a free A-pose preview image from measurements (no credit deducted)."""

    bl_idname = "somata.preview_body"
    bl_label = "Generate Preview"
    bl_description = "Generate a free A-pose reference image from measurements"

    gender: EnumProperty(
        name="Gender",
        items=[("male", "Male", ""), ("female", "Female", "")],
        default="female",
    )
    height_cm: FloatProperty(name="Height (cm)", default=170.0, min=140.0, max=220.0)
    weight_kg: FloatProperty(name="Weight (kg)", default=65.0, min=40.0, max=180.0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=280)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "gender")
        layout.prop(self, "height_cm")
        layout.prop(self, "weight_kg")

    def execute(self, context):
        client = get_client()

        def do_preview():
            return client.preview_body(
                gender=self.gender,
                height_cm=self.height_cm,
                weight_kg=self.weight_kg,
            )

        def on_done(result):
            # Store token on the scene so the Confirm operator can use it
            context.scene.somata_preview_token = result["previewToken"]
            context.scene.somata_preview_url = result["previewUrl"]
            self.report({"INFO"}, "Preview ready — check the Somata panel to confirm.")

        def on_error(err):
            msg = err.message if isinstance(err, SomataError) else str(err)
            if getattr(err, "status", None) == 422:
                msg = "Preview blocked by NSFW filter. Adjust the inputs and try again."
            self.report({"ERROR"}, msg)

        self.report({"INFO"}, "Generating preview…")
        async_call(do_preview, on_done=on_done, on_error=on_error)
        return {"FINISHED"}


class SomataGenerateBody(bpy.types.Operator):
    """Confirm a preview and generate the full 3D mesh (deducts 1 credit)."""

    bl_idname = "somata.generate_body"
    bl_label = "Generate Mesh (1 credit)"
    bl_description = "Confirm this preview and generate the full FBX mesh — costs 1 credit"

    asset_name: StringProperty(name="Name")
    gender: EnumProperty(
        name="Gender",
        items=[("male", "Male", ""), ("female", "Female", "")],
        default="female",
    )
    height_cm: FloatProperty(name="Height (cm)", default=170.0, min=140.0, max=220.0)
    weight_kg: FloatProperty(name="Weight (kg)", default=65.0, min=40.0, max=180.0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=280)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "asset_name")
        layout.prop(self, "gender")
        layout.prop(self, "height_cm")
        layout.prop(self, "weight_kg")

    def execute(self, context):
        token = getattr(context.scene, "somata_preview_token", "")
        if not token:
            self.report({"ERROR"}, "No preview token — run Generate Preview first.")
            return {"CANCELLED"}

        client = get_client()

        def do_generate():
            return client.generate_body(
                preview_token=token,
                name=self.asset_name,
                gender=self.gender,
                height_cm=self.height_cm,
                weight_kg=self.weight_kg,
            )

        def on_done(asset):
            context.scene.somata_preview_token = ""
            context.scene.somata_preview_url = ""
            self.report({"INFO"}, f"Asset '{asset['name']}' created — mesh generating in background.")

        def on_error(err):
            msg = err.message if isinstance(err, SomataError) else str(err)
            if getattr(err, "status", None) == 402:
                msg = "No credits remaining. Upgrade your plan at /pricing."
            self.report({"ERROR"}, msg)

        self.report({"INFO"}, "Confirming — 1 credit will be deducted…")
        async_call(do_generate, on_done=on_done, on_error=on_error)
        return {"FINISHED"}


# ── Scene properties to hold transient preview state ─────────────────────────

def register_scene_props():
    bpy.types.Scene.somata_preview_token = bpy.props.StringProperty(default="")
    bpy.types.Scene.somata_preview_url = bpy.props.StringProperty(default="")


def unregister_scene_props():
    del bpy.types.Scene.somata_preview_token
    del bpy.types.Scene.somata_preview_url
