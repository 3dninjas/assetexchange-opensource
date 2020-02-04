plugin_info = {
    "name": "Asset Ninja Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Niklas Salmoukas",
    "version": "1.0.0"
}

import assetexchange_maya
import assetimport_maya

def initializePlugin(mobject):
    assetexchange_maya.register_plugin("assetninja.extension.maya.assetimport", plugin_info, assetimport_maya.AssetPushService)

def uninitializePlugin(mobject):
    assetexchange_maya.unregister_plugin("assetninja.extension.maya.assetimport")
