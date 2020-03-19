plugin_info = {
    "name": "Asset Ninja Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Niklas Salmoukas",
    "version": "1.0.0"
}

# !!! PACK HERE !!!
try:
    import assetexchange_houdini
    import assetimport_houdini

    def initializePlugin():
        assetexchange_houdini.register_plugin("assetninja.extension.houdini.assetimport", plugin_info, assetimport_houdini.AssetPushService)
        print "init done"
    def uninitializePlugin():
        assetexchange_houdini.unregister_plugin("assetninja.extension.houdini.assetimport")
        print "uninit done"
except:
    print "failed import and start plugin"
