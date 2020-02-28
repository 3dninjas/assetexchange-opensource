bl_info = {
    "name": "Asset Ninja Space Probe",
    "description": "Handles all low level requests from Asset Ninja.",
    "author": "Niklas Salmoukas",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "None",
    "wiki_url": "https://github.com/assetninja/assetexchange/wiki",
    "tracker_url": "https://github.com/assetninja/assetexchange/issues",
    "support": "COMMUNITY",
    "category": "Object"
}

# !!! PACK HERE !!!

import assetexchange_blender
import spaceprobe_blender


def register():
    assetexchange_blender.register_addon(
        "assetninja.extension.blender.spaceprobe",
        bl_info, None,
        { "assetninja.extension.blender.spaceprobe#1": spaceprobe_blender.SpaceProbeService }
    )


def unregister():
    assetexchange_blender.unregister_addon("assetninja.extension.blender.spaceprobe")
