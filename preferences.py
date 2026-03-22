import bpy
from bpy.props import StringProperty
from bpy.types import AddonPreferences


class SomataPreferences(AddonPreferences):
    bl_idname = __package__

    api_url: StringProperty(
        name="API URL",
        default="http://localhost:3001",
        description="Somata API base URL",
    )

    # JWT stored in preferences — persists across sessions.
    # Never logged or exposed in the UI beyond a masked display.
    token: StringProperty(
        name="Token",
        default="",
        options={"HIDDEN"},
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_url")
        if self.token:
            layout.label(text="Logged in", icon="CHECKMARK")
            layout.operator("somata.logout", icon="X")
        else:
            layout.label(text="Not logged in", icon="ERROR")
