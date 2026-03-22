bl_info = {
    "name": "Somata",
    "author": "Somata",
    "version": (0, 1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Somata",
    "description": "Generate and import photorealistic digital human meshes via Somata",
    "doc_url": "https://github.com/3pda/somata-blender",
    "category": "Import-Export",
}

import bpy

from .preferences import SomataPreferences
from .operators import register as register_operators, unregister as unregister_operators
from .panels import register as register_panels, unregister as unregister_panels


def register():
    bpy.utils.register_class(SomataPreferences)
    register_operators()
    register_panels()


def unregister():
    unregister_panels()
    unregister_operators()
    bpy.utils.unregister_class(SomataPreferences)


if __name__ == "__main__":
    register()
