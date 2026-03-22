"""
Utilities for running blocking API calls off the main thread so Blender's
UI stays responsive. Pattern:

    def execute(self, context):
        async_call(
            fn=lambda: client.list_assets(),
            on_done=lambda result: ...,
            on_error=lambda err: self.report({'ERROR'}, str(err)),
        )
        return {'RUNNING_MODAL'}
"""

import threading
import bpy


def async_call(fn, on_done=None, on_error=None):
    """Run fn() in a background thread; schedule callbacks on the main thread."""
    def run():
        try:
            result = fn()
            if on_done:
                bpy.app.timers.register(lambda: on_done(result) or None, first_interval=0)
        except Exception as e:
            if on_error:
                bpy.app.timers.register(lambda: on_error(e) or None, first_interval=0)

    threading.Thread(target=run, daemon=True).start()


def get_prefs(context=None):
    """Return the addon preferences."""
    return bpy.context.preferences.addons[__package__].preferences


def get_client():
    """Return a configured SomataClient for the current session."""
    from .api import SomataClient
    prefs = get_prefs()
    return SomataClient(base_url=prefs.api_url, token=prefs.token)
