import c4d
import assetexchange_shared
import assetexchange_c4d
from . import importer

REDSHIFT_ID = 1036219

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
    # @assetexchange_c4d.execute_on_main_thread
    def Push(self, data):
        #Adding 'doc' to scope!
        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()

        if rd[c4d.RDATA_RENDERENGINE] == REDSHIFT_ID:
            if data['asset']['typeUid'] == 'environment.hdri':
                importer.environment_hdri(doc, data['asset'], data['selectedVariants'])
                return True
            if data['asset']['typeUid'] == 'surface.maps':
                importer.surface_maps_rs(doc, data['asset'], data['selectedVariants'])
                return True

        if data['asset']['typeUid'] == 'environment.hdri':
            importer.environment_hdri(doc, data['asset'], data['selectedVariants'])
            return True
        if data['asset']['typeUid'] == 'surface.maps':
            importer.surface_maps(doc, data['asset'], data['selectedVariants'])
            return True

        return False
