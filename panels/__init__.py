import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty
from .sidebar import SomataPanel, SomataAssetsPanel

classes = (
    SomataPanel,
    SomataAssetsPanel,
)


def register():
    _register_upload_props()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    _unregister_upload_props()


def _register_upload_props():
    bpy.types.Scene.somata_upload_name = StringProperty(
        name="Name",
        description="Asset name in Somata",
        default="",
    )
    bpy.types.Scene.somata_upload_height = FloatProperty(
        name="Height (cm)",
        default=170.0,
        min=100.0,
        max=250.0,
    )
    bpy.types.Scene.somata_upload_weight = FloatProperty(
        name="Weight (kg)",
        default=65.0,
        min=30.0,
        max=200.0,
    )
    bpy.types.Scene.somata_upload_gender = EnumProperty(
        name="Gender",
        items=[("male", "Male", ""), ("female", "Female", "")],
        default="female",
    )


def _unregister_upload_props():
    del bpy.types.Scene.somata_upload_name
    del bpy.types.Scene.somata_upload_height
    del bpy.types.Scene.somata_upload_weight
    del bpy.types.Scene.somata_upload_gender
