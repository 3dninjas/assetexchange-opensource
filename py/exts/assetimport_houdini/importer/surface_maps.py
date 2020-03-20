import assetexchange_shared
import os
import hou


def map_maps(shader_name, surface_maps, shader):

    shader_name = str(shader_name)

    if locals().get("hou_parent") is None:
        hou_parent = hou.node("/mat")
    
    hou_node = hou_parent.createNode("principledshader::2.0", shader_name, 
                                    run_init_scripts=False, load_contents=True, exact_type_name=True)
    node_name = str("/mat/"+shader_name)

    if "Diffuse" in surface_maps:
        diffuse = str(surface_maps["Diffuse"]["file"]["path"])
        if locals().get("hou_node") is None:
            hou_node = hou.node(node_name)
        hou_parm = hou_node.parm("basecolor_useTexture")
        hou_parm.lock(False)
        hou_parm.set(1)
        hou_parm = hou_node.parm("basecolor_texture")
        hou_parm.lock(False)
        hou_parm.set(diffuse)
        hou_parm.setAutoscope(False)

    if "Albedo" in surface_maps:
        diffuse = str(surface_maps["Albedo"]["file"]["path"])

        if locals().get("hou_node") is None:
            hou_node = hou.node(node_name)
        hou_parm = hou_node.parm("basecolor_useTexture")
        hou_parm.lock(False)
        hou_parm.set(1)
        hou_parm = hou_node.parm("basecolor_texture")
        hou_parm.lock(False)
        hou_parm.set(diffuse)
        hou_parm.setAutoscope(False)

    if "Roughness" in surface_maps:
        rough = str(surface_maps["Roughness"]["file"]["path"])

        if locals().get("hou_node") is None:
            hou_node = hou.node(node_name)
        hou_parm = hou_node.parm("rough_useTexture")
        hou_parm.lock(False)
        hou_parm.set(1)
        hou_parm = hou_node.parm("rough_texture")
        hou_parm.lock(False)
        hou_parm.set(rough)
        hou_parm.setAutoscope(False)
        hou_parm = hou_node.parm("rough_monoChannel")
        hou_parm.lock(False)
        hou_parm.set(1)
        hou_parm = hou_node.parm("rough_textureColorSpace")
        hou_parm.lock(False)
        hou_parm.set("linear")
        hou_parm.setAutoscope(False)

    if "Normal" in surface_maps:
        normal = str(surface_maps["Normal"]["file"]["path"])
        if locals().get("hou_node") is None:
            hou_node = hou.node(node_name)
        hou_parm = hou_node.parm("baseBumpAndNormal_enable")
        hou_parm.lock(False)
        hou_parm.set(1)
        hou_parm = hou_node.parm("baseBumpAndNormal_type")
        hou_parm.lock(False)
        hou_parm.set("normal")
        hou_parm = hou_node.parm("baseBump_colorSpace")
        hou_parm.lock(False)
        hou_parm.set("linear")
        hou_parm = hou_node.parm("baseBump_bumpScale")
        hou_parm.lock(False)
        hou_parm.set(0.0501)
        hou_parm = hou_node.parm("baseNormal_texture")
        hou_parm.lock(False)
        hou_parm.set(normal)
        hou_parm.setAutoscope(False)

    if "Displacement" in surface_maps:
        displace = str(surface_maps["Displacement"]["file"]["path"])
        if locals().get("hou_node") is None:
            hou_node = hou.node(node_name)
        hou_parm = hou_node.parm("dispTex_enable")
        hou_parm.lock(False)
        hou_parm.set(1)
        hou_parm = hou_node.parm("dispTex_texture")
        hou_parm.lock(False)
        hou_parm.set(displace)
        hou_parm.setAutoscope(False)



def surface_maps(asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get all maps and convert to dictionary by map type
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        surface_maps = {surface_map["type"]: surface_map for surface_map in object_list}

        shader_name = asset['uid'].split(".")[1]
        shader_type = "principled"
        map_maps(shader_name, surface_maps, shader_type)
