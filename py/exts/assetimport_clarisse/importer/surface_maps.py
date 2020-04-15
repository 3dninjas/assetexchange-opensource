import assetexchange_shared
import os, re
import ix


def map_maps(shader_name, surface_maps, shader):
    ix.log_info("Creating Basic shader setup.")
    shader_name = str(shader_name)
    default_ctx = ix.cmds.CreateContext(shader_name, "Global", "project://scene")
    
    if shader == "disney":
        material = ix.cmds.CreateObject(shader_name, "MaterialPhysicalDisneyPrincipled", "Global", default_ctx)

        if "Diffuse" in surface_maps:
            diffuse = str(surface_maps["Diffuse"]["file"]["path"])
            channel_name = shader_name+"_Diffuse"
            tx = ix.cmds.CreateObject(channel_name, 'TextureMapFile', default_ctx)
            tx.attrs.filename = diffuse
            tx.attrs.color_space_auto_detect = 0
            tx.attrs.mipmap_filtering_mode = 1
            tx.attrs.file_color_space = 'Clarisse|sRGB'
            set_tex = str(default_ctx)+"/"+str(shader_name)
            ix.cmds.SetTexture([set_tex+".base_color"], set_tex+"_Diffuse")

        if "Albedo" in surface_maps:
            albedo = str(surface_maps["Albedo"]["file"]["path"])
            channel_name = shader_name+"_Albedo"
            tx = ix.cmds.CreateObject(channel_name, 'TextureMapFile', default_ctx)
            tx.attrs.filename = albedo
            tx.attrs.color_space_auto_detect = 0
            tx.attrs.mipmap_filtering_mode = 1
            tx.attrs.file_color_space = 'Clarisse|sRGB'
            set_tex = str(default_ctx)+"/"+str(shader_name)
            ix.cmds.SetTexture([set_tex+".base_color"], set_tex+"_Albedo")

        if "Roughness" in surface_maps:
            rough = str(surface_maps["Roughness"]["file"]["path"])
            channel_name = shader_name+"_Roughness"
            tx = ix.cmds.CreateObject(channel_name, 'TextureMapFile', default_ctx)
            tx.attrs.filename = rough
            tx.attrs.color_space_auto_detect = 0
            tx.attrs.mipmap_filtering_mode = 1
            tx.attrs.file_color_space = 'linear'
            set_tex = str(default_ctx)+"/"+str(shader_name)
            ix.cmds.SetTexture([set_tex+".roughness"], set_tex+"_Roughness")
            ix.cmds.SetValues([set_tex+"_Roughness.single_channel_file_behavior"], ["1"])
            ix.cmds.SetValues([set_tex+".specular"], ["0.2"])

        if "Normal" in surface_maps:
            normal = str(surface_maps["Normal"]["file"]["path"])
            channel_name = shader_name+"_Normal"
            tx = ix.cmds.CreateObject(channel_name, 'TextureMapFile', default_ctx)
            tx.attrs.filename = normal
            tx.attrs.color_space_auto_detect = 0
            tx.attrs.mipmap_filtering_mode = 1
            tx.attrs.file_color_space = 'linear'
            txnrm_util=ix.cmds.CreateObject(channel_name+"_nrm", "TextureNormalMap", default_ctx)
            set_tex = str(default_ctx)+"/"+str(shader_name)
            ix.cmds.SetTexture([set_tex+".normal_input"], set_tex+"_Normal_nrm")
            ix.cmds.SetTexture([set_tex+"_Normal_nrm.input"], set_tex+"_Normal")

        if "Displacement" in surface_maps:
            displacement = str(surface_maps["Displacement"]["file"]["path"])
            channel_name = shader_name+"_Displacement"
            tx = ix.cmds.CreateObject(channel_name, 'TextureMapFile', default_ctx)
            displ_node = ix.cmds.CreateObject(channel_name+"_displacement", "Displacement", default_ctx)
            tx.attrs.filename = displacement
            tx.attrs.color_space_auto_detect = 0
            tx.attrs.mipmap_filtering_mode = 1
            tx.attrs.file_color_space = 'linear'
            tx.attrs.use_raw_data = "1"
            ix.cmds.SetTexture([set_tex+"_Displacement_displacement.front_value"], set_tex+"_Displacement")
            ix.cmds.SetValues([set_tex+"_Displacement.single_channel_file_behavior"], ["1"])
            ix.cmds.SetValues([set_tex+"_Displacement_displacement.front_value"], ["0.07"])




def surface_maps(asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get all maps and convert to dictionary by map type
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        surface_maps = {surface_map["type"]: surface_map for surface_map in object_list}

        shader_name = asset['uid'].split(".")[1]
        
        #normalize names to underscore
        shader_name = shader_name.replace("-","_")
        
        shader_type = "disney"
        map_maps(shader_name, surface_maps, shader_type)
        ix.log_info("Basic shader setup created.")
