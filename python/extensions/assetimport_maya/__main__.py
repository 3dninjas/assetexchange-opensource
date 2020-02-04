import assetexchange_maya
import assetimport_maya

def initializePlugin(mobject):
    assetexchange_maya.register_plugin("assetninja.extension.maya.assetimport", assetimport_maya.AssetPushService)

def uninitializePlugin(mobject):
    assetexchange_maya.unregister_plugin("assetninja.extension.maya.assetimport")
