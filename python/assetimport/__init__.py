bl_info = {
    "name": "Asset Ninja Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Niklas Salmoukas",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "None",
    "wiki_url": "https://github.com/core-process/assetninja/wiki",
    "tracker_url": "https://github.com/core-process/assetninja/issues",
    "support": "COMMUNITY",
    "category": "Object"
}

import rpcninja.shared.server.interfaces as rpcninja_interfaces
import rpcninja.blender.threading as rpcninja_threading
import rpcninja.blender.addon as rpcninja_addon
import rpcninja.shared.asset.variants as asset_variants
import bpy


def _import_environment_hdri(asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = asset_variants.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get environment map
        object_list = asset_variants.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
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
            nodes.get("World Output").inputs[0], env_text_node.outputs[0])


def _import_surface_maps(asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = asset_variants.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get all maps and convert to dictionary by map type
        object_list = asset_variants.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        surface_maps = {surface_map["type"]: surface_map for surface_map in object_list}

        # create material object
        mat_name = asset['uid'] + "_" + "_".join(variantConfig)
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True

        # helper and lookup variables
        nodes = mat.node_tree.nodes

        node_y_next = 800
        node_y_delta = 400
        node_x = -500

        # add diffuse
        if "Diffuse" in surface_maps:
            # texture node
            diff_tex_node = nodes.new('ShaderNodeTexImage')
            diff_tex_node.image = bpy.data.images.load(surface_maps["Diffuse"]["file"]["path"])
            diff_tex_node.show_texture = True
            diff_tex_node.image.colorspace_settings.name = "sRGB"
            # link to bsdf
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs[0], diff_tex_node.outputs[0])
            # position node
            diff_tex_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta

        # add specular
        if "Specular" in surface_maps:
            # texture node
            spec_tex_node = nodes.new('ShaderNodeTexImage')
            spec_tex_node.image = bpy.data.images.load(surface_maps["Specular"]["file"]["path"])
            spec_tex_node.show_texture = True
            spec_tex_node.image.colorspace_settings.name = "sRGB"
            # link to bsdf
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs[5], spec_tex_node.outputs[0])
            # position node
            spec_tex_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta

        # add roughness
        if "Roughness" in surface_maps:
            # texture node
            rough_tex_node = nodes.new('ShaderNodeTexImage')
            rough_tex_node.image = bpy.data.images.load(surface_maps["Roughness"]["file"]["path"])
            rough_tex_node.show_texture = True
            rough_tex_node.image.colorspace_settings.name = "Non-Color"
            # link to bsdf
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs[7], rough_tex_node.outputs[0])
            # position node
            rough_tex_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta

        # add normal
        if "Normal" in surface_maps:
            # texture node
            norm_tex_node = nodes.new('ShaderNodeTexImage')
            norm_tex_node.image = bpy.data.images.load(surface_maps["Normal"]["file"]["path"])
            norm_tex_node.show_texture = True
            norm_tex_node.image.colorspace_settings.name = "Non-Color"
            # normal map node
            norm_map_node = nodes.new("ShaderNodeNormalMap")
            norm_map_node.space = "TANGENT"
            norm_map_node.uv_map = "UVMap"
            # link to bsdf
            mat.node_tree.links.new(
                norm_map_node.inputs[1], norm_tex_node.outputs[0])
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs[19], norm_map_node.outputs[0])
            # position node
            norm_tex_node.location = (node_x - 400, node_y_next)
            norm_map_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta

        # add displacement
        if "Displacement" in surface_maps:
            # displacement node
            disp_node = nodes.new("ShaderNodeDisplacement")
            disp_node.inputs[0].default_value = 0.1
            disp_node.inputs[1].default_value = 0
            # texture node
            disp_tex_node = nodes.new('ShaderNodeTexImage')
            disp_tex_node.image = bpy.data.images.load(surface_maps["Displacement"]["file"]["path"])
            disp_tex_node.show_texture = True
            disp_tex_node.image.colorspace_settings.name = "Non-Color"
            # link to bsdf
            mat.node_tree.links.new(
                disp_node.inputs[2], disp_tex_node.outputs[0])
            mat.node_tree.links.new(
                nodes.get("Material Output").inputs[2], disp_node.outputs[0])
            # enable displacement
            mat.cycles.displacement_method = 'BOTH'
            # position
            disp_tex_node.location = (node_x - 400, node_y_next)
            disp_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta


class AssetPushService(rpcninja_interfaces.AssetPushServiceInterface):
    # lists all supported asset types which can be pushed here
    def SupportedTypes(self, _):
        return [
            'environment.hdri',
            'mesh+surface.maps',
            'surface.maps',
        ]

    # checks if specific asset can be pushed here
    def PushAllowed(self, asset):
        return True

    # asset gets pushed here
    @rpcninja_threading.execute_on_main_thread
    def Push(self, data):
        if data['asset']['typeUid'] == 'environment.hdri':
            _import_environment_hdri(data['asset'], data['selectedVariants'])
            return True
        if data['asset']['typeUid'] == 'surface.maps':
            _import_surface_maps(data['asset'], data['selectedVariants'])
            return True
        return False


def register():
    rpcninja_addon.start("assetninja.extension.blender.assetimport", bl_info, AssetPushService)


def unregister():
    rpcninja_addon.stop()
