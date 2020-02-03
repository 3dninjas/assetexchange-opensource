bl_info = {
    "name": "Asset Ninja Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Niklas Salmoukas",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "None",
    "wiki_url": "https://github.com/assetninja/assetexchange/wiki",
    "tracker_url": "https://github.com/assetninja/assetexchange/issues",
    "support": "COMMUNITY",
    "category": "Object"
}

import assetexchange_shared
import assetexchange_blender
from . import importer

class AssetPushService(assetexchange_shared.server.AssetPushServiceInterface):
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
    @assetexchange_blender.execute_on_main_thread
    def Push(self, data):
        if data['asset']['typeUid'] == 'environment.hdri':
            importer.environment_hdri(data['asset'], data['selectedVariants'])
            return True
        if data['asset']['typeUid'] == 'surface.maps':
            importer.surface_maps(data['asset'], data['selectedVariants'])
            return True
        return False


def register():
    assetexchange_blender.register_addon("assetninja.extension.blender.assetimport", bl_info, AssetPushService)


def unregister():
    assetexchange_blender.unregister_addon("assetninja.extension.blender.assetimport")
