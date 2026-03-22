import bpy
from bpy.props import StringProperty
from ..utils import async_call, get_client
from ..api.client import SomataClient, SomataError


class SomataLogin(bpy.types.Operator):
    bl_idname = "somata.login"
    bl_label = "Log In"
    bl_description = "Log in to your Somata account"

    email: StringProperty(name="Email")
    password: StringProperty(name="Password", subtype="PASSWORD")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=320)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "email")
        layout.prop(self, "password")

    def execute(self, context):
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences
        client = SomataClient(base_url=prefs.api_url)

        def do_login():
            return client.login(self.email, self.password)

        def on_done(result):
            prefs.token = result["token"]
            self.report({"INFO"}, f"Logged in as {result['user']['email']}")

        def on_error(err):
            msg = err.message if isinstance(err, SomataError) else str(err)
            self.report({"ERROR"}, f"Login failed: {msg}")

        async_call(do_login, on_done=on_done, on_error=on_error)
        return {"FINISHED"}


class SomataLogout(bpy.types.Operator):
    bl_idname = "somata.logout"
    bl_label = "Log Out"
    bl_description = "Clear saved credentials"

    def execute(self, context):
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences
        prefs.token = ""
        self.report({"INFO"}, "Logged out")
        return {"FINISHED"}
