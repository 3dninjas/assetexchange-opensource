import assetexchange_maya

def initializePlugin(mobject):
    assetexchange_maya.register_plugin("assetninja.extension.maya.assetimport")

def uninitializePlugin(mobject):
    assetexchange_maya.unregister_plugin("assetninja.extension.maya.assetimport")
