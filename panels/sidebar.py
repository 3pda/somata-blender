import bpy
from ..operators.assets import get_cache

PKG = __package__.split(".")[0]  # "somata_blender"

STATUS_ICONS = {
    "READY": "CHECKMARK",
    "PROCESSING": "SORTTIME",
    "SIGNING": "SORTTIME",
    "PENDING": "SORTTIME",
    "FAILED": "ERROR",
}


def _prefs(context):
    return context.preferences.addons[PKG].preferences


class SomataPanel(bpy.types.Panel):
    """Main Somata panel — login, upload settings, and creation actions."""

    bl_label = "Somata"
    bl_idname = "VIEW3D_PT_somata"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Somata"

    def draw(self, context):
        layout = self.layout
        prefs = _prefs(context)
        scene = context.scene

        # ── Auth state ───────────────────────────────────────────────────────
        if not prefs.token:
            layout.label(text="Not logged in", icon="USER")
            layout.operator("somata.login", icon="LOCKED")
            return

        layout.label(text="Logged in", icon="CHECKMARK")
        layout.operator("somata.logout", text="Log Out", icon="X")
        layout.separator()

        # ── Upload Photo ─────────────────────────────────────────────────────
        box = layout.box()
        box.label(text="From Photo", icon="IMAGE_DATA")

        col = box.column(align=True)
        col.prop(scene, "somata_upload_name")
        col.prop(scene, "somata_upload_gender")

        row = box.row(align=True)
        row.prop(scene, "somata_upload_height")
        row.prop(scene, "somata_upload_weight")

        box.operator("somata.upload_photo", icon="FILEBROWSER")

        layout.separator()

        # ── Generate Body ────────────────────────────────────────────────────
        box = layout.box()
        box.label(text="From Measurements", icon="ARMATURE_DATA")

        preview_token = scene.somata_preview_token
        preview_url = scene.somata_preview_url

        if preview_token:
            box.label(text="Preview ready — confirm to generate mesh", icon="CHECKMARK")
            box.operator("somata.generate_body", icon="MESH_MONKEY")
            box.operator("somata.preview_body", text="Regenerate Preview", icon="FILE_REFRESH")
        else:
            box.operator("somata.preview_body", icon="RENDER_STILL")


class SomataAssetsPanel(bpy.types.Panel):
    """Asset library — list assets, show status, and import READY meshes."""

    bl_label = "My Assets"
    bl_idname = "VIEW3D_PT_somata_assets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Somata"
    bl_parent_id = "VIEW3D_PT_somata"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return bool(_prefs(context).token)

    def draw(self, context):
        layout = self.layout
        assets = get_cache()

        layout.operator("somata.refresh_assets", icon="FILE_REFRESH",
                        text="Refresh" if assets else "Load Assets")

        if not assets:
            layout.label(text="No assets yet.", icon="INFO")
            return

        layout.separator()
        for asset in assets:
            status = asset.get("status", "?")
            icon = STATUS_ICONS.get(status, "QUESTION")

            row = layout.row(align=True)
            row.label(text=asset.get("name", "Unnamed")[:28], icon=icon)
            row.label(text=status)
            if status == "READY":
                op = row.operator("somata.download_mesh", text="", icon="IMPORT")
                op.asset_id = asset["id"]
