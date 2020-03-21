import assetexchange_shared
import assetexchange_houdini
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
    @assetexchange_houdini.execute_on_main_thread
    def Push(self, data):
        if data['asset']['typeUid'] == 'environment.hdri':
            importer.environment_hdri(data['asset'], data['selectedVariants'])
            return True
        if data['asset']['typeUid'] == 'surface.maps':
            importer.surface_maps(data['asset'], data['selectedVariants'])
            return True
        return False
