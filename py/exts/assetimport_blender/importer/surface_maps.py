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
        coord.location = (-2000, 300)

        mapping = nodes.new('ShaderNodeMapping')
        mapping.location = (-1600, 300)
        mat.node_tree.links.new(coord.outputs['UV'], mapping.inputs['Vector'])

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
                nodes.get("Principled BSDF").inputs['Base Color'], diff_tex_node.outputs['Color'])
            # position node
            diff_tex_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], diff_tex_node.inputs['Vector'])

        # add metalness
        if "Metalness" in surface_maps:
            # texture node
            met_tex_node = nodes.new("ShaderNodeTexImage")
            met_tex_node.image = bpy.data.images.load(surface_maps["Metalness"]["file"]["path"])
            met_tex_node.show_texture = True
            met_tex_node.image.colorspace_settings.name = "Non-Color"
            # link to bsdf
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs['Metallic'], met_tex_node.outputs['Color'])
            # position node
            met_tex_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], met_tex_node.inputs['Vector'])

        # add specular
        if "Specular" in surface_maps and not "Metalness" in surface_maps:
            # texture node
            spec_tex_node = nodes.new('ShaderNodeTexImage')
            spec_tex_node.image = bpy.data.images.load(surface_maps["Specular"]["file"]["path"])
            spec_tex_node.show_texture = True
            spec_tex_node.image.colorspace_settings.name = "Non-Color"
            # link to bsdf
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs['Specular'], spec_tex_node.outputs['Color'])
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
                nodes.get("Principled BSDF").inputs['Roughness'], rough_tex_node.outputs['Color'])
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
            # normal map node
            norm_map_node = nodes.new("ShaderNodeNormalMap")
            norm_map_node.space = "TANGENT"
            norm_map_node.uv_map = "UVMap"

            # check for whether map is using opengl or directx
            handedness_ogl = surface_maps["Normal"]["details"].get("handedness", "right") == "right"

            if handedness_ogl:
                # link the image texture and normal node
                mat.node_tree.links.new(
                    norm_map_node.inputs['Color'], norm_tex_node.outputs['Color'])
            else:
                # invert node
                norm_curve_node = nodes.new("ShaderNodeRGBCurve")
                norm_curve_node.mapping.initialize()
                norm_curve_node.mapping.curves[1].points[0].location[1] = 1
                norm_curve_node.mapping.curves[1].points[1].location[1] = 0
                norm_curve_node.mapping.update()
                norm_curve_node.mute = handedness_ogl
                norm_curve_node.location = (node_x - 400, node_y_next)

                # link the image texture, rgb curves and normal node
                mat.node_tree.links.new(
                    norm_curve_node.inputs['Color'], norm_tex_node.outputs['Color'])
                mat.node_tree.links.new(
                    norm_map_node.inputs['Color'], norm_curve_node.outputs['Color'])

            # link to bsdf
            mat.node_tree.links.new(
                nodes.get("Principled BSDF").inputs['Normal'], norm_map_node.outputs['Normal'])
            # position node
            norm_tex_node.location = (node_x - 800, node_y_next)
            norm_map_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], norm_tex_node.inputs['Vector'])

        # add displacement
        if "Displacement" in surface_maps:
            # displacement node
            disp_node = nodes.new("ShaderNodeDisplacement")
            disp_node.inputs['Midlevel'].default_value = 0
            disp_node.inputs['Scale'].default_value = 0.1
            # texture node
            disp_tex_node = nodes.new('ShaderNodeTexImage')
            disp_tex_node.image = bpy.data.images.load(surface_maps["Displacement"]["file"]["path"])
            disp_tex_node.show_texture = True
            disp_tex_node.image.colorspace_settings.name = "Non-Color"
            # link to bsdf
            mat.node_tree.links.new(
                disp_node.inputs['Height'], disp_tex_node.outputs['Color'])
            mat.node_tree.links.new(
                nodes.get("Material Output").inputs['Displacement'], disp_node.outputs['Displacement'])
            # enable displacement
            mat.cycles.displacement_method = 'BOTH'
            # position
            disp_tex_node.location = (node_x - 400, node_y_next)
            disp_node.location = (node_x, node_y_next)
            node_y_next -= node_y_delta
            # connect to mapping
            mat.node_tree.links.new(mapping.outputs['Vector'], disp_tex_node.inputs['Vector'])
