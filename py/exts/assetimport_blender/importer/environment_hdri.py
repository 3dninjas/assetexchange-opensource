import bpy
import assetexchange_shared

def environment_hdri(asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get environment map
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        if len(object_list) == 0:
            return
        env_map = object_list[0]

        # enable world nodes
        world = bpy.data.worlds['World']
        world.use_nodes = True
        nodes = world.node_tree.nodes
        
        # create texture node
        env_text_node = nodes.new('ShaderNodeTexEnvironment')
        env_text_node.image = bpy.data.images.load(env_map["file"]["path"])
        env_text_node.show_texture = True
        env_text_node.image.colorspace_settings.name = "Linear"

        # link to world
        world.node_tree.links.new(
            nodes.get("Background").inputs['Color'], env_text_node.outputs['Color'])
