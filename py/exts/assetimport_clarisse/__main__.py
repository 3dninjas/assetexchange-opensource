plugin_info = {
    "name": "Asset Ninja Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Aleks Katunar",
    "version": "1.0.0",
}

# !!! PACK HERE !!!

import assetexchange_clarisse
import assetimport_clarisse

assetexchange_clarisse.register_plugin("assetninja.extension.clarisse.assetimport", plugin_info, assetimport_clarisse.AssetPushService)
