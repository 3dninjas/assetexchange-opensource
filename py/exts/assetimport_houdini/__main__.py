plugin_info = {
    "name": "Asset Ninja Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Niklas Salmoukas",
    "version": "1.0.0"
}

# !!! PACK HERE !!!

import assetexchange_houdini
import assetimport_houdini

assetexchange_houdini.register_plugin("assetninja.extension.houdini.assetimport", plugin_info, assetimport_houdini.AssetPushService)
