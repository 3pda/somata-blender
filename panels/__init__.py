from .sidebar import SomataPanel, SomataAssetsPanel

classes = (
    SomataPanel,
    SomataAssetsPanel,
)


def register():
    import bpy
    from ..operators.generate_body import register_scene_props
    register_scene_props()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    import bpy
    from ..operators.generate_body import unregister_scene_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    unregister_scene_props()
