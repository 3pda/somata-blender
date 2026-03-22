import bpy


PKG = __package__.split(".")[0]  # "somata_blender"


def _prefs(context):
    return context.preferences.addons[PKG].preferences


class SomataPanel(bpy.types.Panel):
    """Main Somata panel — login status, credits, and creation actions."""

    bl_label = "Somata"
    bl_idname = "VIEW3D_PT_somata"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Somata"

    def draw(self, context):
        layout = self.layout
        prefs = _prefs(context)

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
        box.operator("somata.upload_photo", icon="IMPORT")

        layout.separator()

        # ── Generate Body ────────────────────────────────────────────────────
        box = layout.box()
        box.label(text="From Measurements", icon="ARMATURE_DATA")

        preview_token = getattr(context.scene, "somata_preview_token", "")
        preview_url = getattr(context.scene, "somata_preview_url", "")

        if preview_token:
            box.label(text="Preview ready", icon="CHECKMARK")
            if preview_url:
                box.label(text=preview_url[:48] + "…" if len(preview_url) > 48 else preview_url)
            box.operator("somata.generate_body", icon="MESH_MONKEY")
            box.operator("somata.preview_body", text="Regenerate Preview", icon="FILE_REFRESH")
        else:
            box.operator("somata.preview_body", icon="RENDER_STILL")


class SomataAssetsPanel(bpy.types.Panel):
    """Asset library — list READY assets and import them."""

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
        assets = getattr(context.scene, "somata_assets_cache", [])

        if not assets:
            layout.label(text="No assets loaded yet.")
            layout.operator("somata.refresh_assets", icon="FILE_REFRESH")
            return

        for asset in assets:
            row = layout.row(align=True)
            status = asset.get("status", "?")
            icon = "CHECKMARK" if status == "READY" else "SORTTIME"
            row.label(text=asset.get("name", "Unnamed"), icon=icon)
            if status == "READY":
                op = row.operator("somata.download_mesh", text="", icon="IMPORT")
                op.asset_id = asset["id"]
