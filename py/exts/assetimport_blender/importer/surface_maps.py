import bpy
import assetexchange_shared

def surface_maps(asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get all maps and convert to dictionary by map type
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
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

        # Texture Mapping nodes
        coord = nodes.new('ShaderNodeTexCoord')
        coord.location = (-1400, 300)

        mapping = nodes.new('ShaderNodeMapping')
        mapping.location = (-1200, 300)
        mat.node_tree.links.new(coord.outputs['UV'], mapping.inputs['Vector'])

        # detect workflow
        is_specular_workflow = "Specular" in surface_maps and not "Metalness" in surface_maps

        # add diffuse
        if "Base Color" in surface_maps or "Albedo" in surface_maps or "Diffuse" in surface_maps:
            # texture node
            diff_tex_node = nodes.new('ShaderNodeTexImage')
            diff_tex_node.image = bpy.data.images.load(
                surface_maps.get("Base Color",
                    surface_maps.get("Albedo",
                        surface_maps.get("Diffuse")))["file"]["path"])
            diff_tex_node.show_texture = True
            diff_tex_node.image.colorspace_settings.name = "sRGB"
            # link to bsdf
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs[0], diff_tex_node.outputs[0])
            # position node
            diff_tex_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], diff_tex_node.inputs['Vector'])

        # add metalness
        if not is_specular_workflow and "Metalness" in surface_maps:
            # texture node
            met_tex_node = nodes.new("ShaderNodeTexImage")
            met_tex_node.image = bpy.data.images.load(surface_maps["Metalness"]["file"]["path"])
            met_tex_node.show_texture = True
            met_tex_node.image.colorspace_settings.name = "Non-Color"
            # link to bsdf
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs[4], met_tex_node.outputs[0])
            # position node
            met_tex_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], met_tex_node.inputs['Vector'])

        # add specular
        if is_specular_workflow and "Specular" in surface_maps:
            # texture node
            spec_tex_node = nodes.new('ShaderNodeTexImage')
            spec_tex_node.image = bpy.data.images.load(surface_maps["Specular"]["file"]["path"])
            spec_tex_node.show_texture = True
            spec_tex_node.image.colorspace_settings.name = "Non-Color"
            # link to bsdf
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs[5], spec_tex_node.outputs[0])
            # position node
            spec_tex_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], spec_tex_node.inputs['Vector'])

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
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], rough_tex_node.inputs['Vector'])

        # add normal
        if "Normal" in surface_maps:
            # texture node
            norm_tex_node = nodes.new("ShaderNodeTexImage")
            norm_tex_node.image = bpy.data.images.load(surface_maps["Normal"]["file"]["path"])
            norm_tex_node.show_texture = True
            norm_tex_node.image.colorspace_settings.name = "Non-Color"
            # invert node
            norm_curve_node = nodes.new("ShaderNodeRGBCurve")
            if surface_maps["Normal"]["details"].get("handedness", "right") == "left":
                norm_curve_node.mapping.initialize()
                norm_curve_node.mapping.curves[1].points[0].location[1] = 1
                norm_curve_node.mapping.curves[1].points[1].location[1] = 0
                norm_curve_node.mapping.update()
            # normal map node
            norm_map_node = nodes.new("ShaderNodeNormalMap")
            norm_map_node.space = "TANGENT"
            norm_map_node.uv_map = "UVMap"
            # link to bsdf
            mat.node_tree.links.new(
                norm_curve_node.inputs[1], norm_tex_node.outputs[0])
            mat.node_tree.links.new(
                norm_map_node.inputs[1], norm_curve_node.outputs[0])
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs[19], norm_map_node.outputs[0])
            # position node
            norm_tex_node.location = (node_x - 800, node_y_next)
            norm_curve_node.location = (node_x - 400, node_y_next)
            norm_map_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], norm_tex_node.inputs['Vector'])

        # add displacement
        if "Displacement" in surface_maps:
            # displacement node
            disp_node = nodes.new("ShaderNodeDisplacement")
            disp_node.inputs[0].default_value = 0.5
            disp_node.inputs[1].default_value = 0.5 - 0.1 * surface_maps["Displacement"]["details"].get("scale", 1)
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
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], disp_tex_node.inputs['Vector'])
