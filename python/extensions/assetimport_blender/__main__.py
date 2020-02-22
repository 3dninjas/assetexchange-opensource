bl_info = {
    "name": "Asset Ninja Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Niklas Salmoukas",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "None",
    "wiki_url": "https://github.com/assetninja/assetexchange/wiki",
    "tracker_url": "https://github.com/assetninja/assetexchange/issues",
    "support": "COMMUNITY",
    "category": "Object"
}

import assetexchange_blender
import assetimport_blender

def register():
    assetexchange_blender.register_addon("assetninja.extension.blender.assetimport", bl_info, assetimport_blender.AssetPushService)


def unregister():
    assetexchange_blender.unregister_addon("assetninja.extension.blender.assetimport")
