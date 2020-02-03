bl_info = {
    "name": "Asset Ninja Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Niklas Salmoukas",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "None",
    "wiki_url": "https://github.com/core-process/assetninja/wiki",
    "tracker_url": "https://github.com/core-process/assetninja/issues",
    "support": "COMMUNITY",
    "category": "Object"
}

# PACK: assetexchange.shared -> ../../../libraries/assetexchange/shared
# PACK: assetexchange.blender -> ../../../libraries/assetexchange/blender
# PACK: .importer -> ./importer

import assetexchange.shared
import assetexchange.blender
from . import importer

class AssetPushService(assetexchange.shared.server.AssetPushServiceInterface):
    # lists all supported asset types which can be pushed here
    def SupportedTypes(self, _):
        return [
            'environment.hdri',
            'mesh+surface.maps',
            'surface.maps',
        ]

    # checks if specific asset can be pushed here
    def PushAllowed(self, asset):
        return True

    # asset gets pushed here
    @assetexchange.blender.execute_on_main_thread
    def Push(self, data):
        if data['asset']['typeUid'] == 'environment.hdri':
            importer.environment_hdri(data['asset'], data['selectedVariants'])
            return True
        if data['asset']['typeUid'] == 'surface.maps':
            importer.surface_maps(data['asset'], data['selectedVariants'])
            return True
        return False


def register():
    assetexchange.blender.register_addon("assetninja.extension.blender.assetimport", bl_info, AssetPushService)


def unregister():
    assetexchange.blender.unregister_addon("assetninja.extension.blender.assetimport")
