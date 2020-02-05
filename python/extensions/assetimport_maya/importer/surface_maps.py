import maya.cmds
import assetexchange_shared

def surface_maps(asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get all maps and convert to dictionary by map type
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        surface_maps = {surface_map["type"]: surface_map for surface_map in object_list}

        # name prefix
        name = asset['uid'].replace(".", "_") + "_" + "_".join(variantConfig)

        # create material node
        mat_node = maya.cmds.shadingNode('aiStandardSurface', asShader=True, name=(name + "_mat"))

        # create shading group
        sg_node = maya.cmds.sets(renderable=True, noSurfaceShader=True, name=(name + "_sg"))
        maya.cmds.defaultNavigation(connectToExisting=True, source=mat_node, destination=sg_node)

        # create texture mapping node
        coords_node = maya.cmds.shadingNode('place2dTexture', asUtility=True, name=(name + "_coords"))

        # add diffuse
        if "Diffuse" in surface_maps:
            # create texture node
            diff_tex_node = maya.cmds.shadingNode('file', asTexture=True, name=(name + "_diff_tex"))
            maya.cmds.setAttr(diff_tex_node+".ftn", surface_maps["Diffuse"]["file"]["path"], type="string")
            maya.cmds.defaultNavigation(connectToExisting=True, source=coords_node, destination=diff_tex_node)
            maya.cmds.setAttr(diff_tex_node+".cs", "sRGB", type="string")
            # link to material
            maya.cmds.connectAttr(diff_tex_node+".outColor", mat_node+".baseColor")

        # add specular
        if "Specular" in surface_maps:
            # create texture node
            spec_tex_node = maya.cmds.shadingNode('file', asTexture=True, name=(name + "_spec_tex"))
            maya.cmds.setAttr(spec_tex_node+".ftn", surface_maps["Specular"]["file"]["path"], type="string")
            maya.cmds.defaultNavigation(connectToExisting=True, source=coords_node, destination=spec_tex_node)
            maya.cmds.setAttr(spec_tex_node+".cs", "Raw", type="string")
            maya.cmds.setAttr(spec_tex_node+".alphaIsLuminance", 1)
            # create range node
            spec_range_node = maya.cmds.shadingNode('aiRange', asShader=True, name=name + "_spec_range")
            maya.cmds.connectAttr(spec_tex_node+".outColor", spec_range_node+".input")
            maya.cmds.connectAttr(spec_range_node+".outColor.outColorR", mat_node+".specular")

        # add roughness
        if "Roughness" in surface_maps:
            # create texture node
            rough_tex_node = maya.cmds.shadingNode('file', asTexture=True, name=(name + "_rough_tex"))
            maya.cmds.setAttr(rough_tex_node+".ftn", surface_maps["Roughness"]["file"]["path"], type="string")
            maya.cmds.defaultNavigation(connectToExisting=True, source=coords_node, destination=rough_tex_node)
            maya.cmds.setAttr(rough_tex_node+".cs", "Raw", type="string")
            maya.cmds.setAttr(rough_tex_node+".alphaIsLuminance", 1)
            # create range node
            rough_range_node = maya.cmds.shadingNode('aiRange', asShader=True, name=name + "_rough_range")
            maya.cmds.connectAttr(rough_tex_node+".outColor", rough_range_node+".input")
            maya.cmds.connectAttr(rough_range_node+".outColor.outColorR", mat_node+".specularRoughness")

        # add normal
        if "Normal" in surface_maps:
            # create texture node
            norm_tex_node = maya.cmds.shadingNode('file', asTexture=True, name=(name + "_norm_tex"))
            maya.cmds.setAttr(norm_tex_node+".ftn", surface_maps["Normal"]["file"]["path"], type="string")
            maya.cmds.defaultNavigation(connectToExisting=True, source=coords_node, destination=norm_tex_node)
            maya.cmds.setAttr(norm_tex_node+".cs", "Raw", type="string")
            # create normal map node
            norm_map_node = maya.cmds.shadingNode('aiNormalMap', asShader=True, name=(name + "_norm_map"))
            maya.cmds.connectAttr(norm_tex_node+".outColor", norm_map_node+".input")
            # link to material
            maya.cmds.connectAttr(norm_map_node+".outValue", mat_node+".normalCamera")

        # add displacement
        if "Displacement" in surface_maps:
            # create texture node
            disp_tex_node = maya.cmds.shadingNode('file', asTexture=True, name=(name + "_disp_tex"))
            maya.cmds.setAttr(disp_tex_node+".ftn", surface_maps["Displacement"]["file"]["path"], type="string")
            maya.cmds.defaultNavigation(connectToExisting=True, source=coords_node, destination=disp_tex_node)
            maya.cmds.setAttr(disp_tex_node+".cs", "Raw", type="string")
            maya.cmds.setAttr(disp_tex_node+".alphaIsLuminance", 1)
            # link to shading group
            maya.cmds.connectAttr(disp_tex_node+".outColor", sg_node+".displacementShader")
