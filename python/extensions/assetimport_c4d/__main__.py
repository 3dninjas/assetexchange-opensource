plugin_info = {
    "name": "Asset Ninja Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Niklas Salmoukas",
    "version": "1.0.0",
    "plugin_id": 1054523,
}

import c4d
import os
import assetexchange_c4d
import assetimport_c4d

class AssetNinjaExtension(c4d.plugins.CommandData):
    def Register(self):
        assetexchange_c4d.register_plugin("assetninja.extension.c4d.assetimport", plugin_info, assetimport_c4d.AssetPushService)

        return c4d.plugins.RegisterCommandPlugin(
            plugin_info['plugin_id'], plugin_info['name'], c4d.PLUGINFLAG_HIDEPLUGINMENU, None,
            plugin_info['description'], self)

if __name__ == '__main__':
    AssetNinjaExtension().Register()
