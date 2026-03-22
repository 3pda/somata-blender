from .auth import SomataLogin, SomataLogout
from .upload_photo import SomataUploadPhoto
from .generate_body import SomataPreviewBody, SomataGenerateBody
from .download_mesh import SomataDownloadMesh
from .assets import SomataRefreshAssets

classes = (
    SomataLogin,
    SomataLogout,
    SomataUploadPhoto,
    SomataPreviewBody,
    SomataGenerateBody,
    SomataDownloadMesh,
    SomataRefreshAssets,
)


def register():
    import bpy
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    import bpy
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
