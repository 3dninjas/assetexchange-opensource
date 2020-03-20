import re
import hou
import assetexchange_shared

def create_dome(name, path,renderer):
    # Initialize parent node variable.
    print("Creating mantra light")
    if locals().get("hou_parent") is None:
        hou_parent = hou.node("/obj")
    
    light_setup = hou_parent.createNode("envlight", name, run_init_scripts=False, 
                                        load_contents=True, exact_type_name=True)
    hou_parm = light_setup.parm("env_map")
    hou_parm.lock(False)
    hou_parm.set(path)
    hou_parm.setAutoscope(False)
    print("Light creation done.")

def environment_hdri(asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants(
        'Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get environment map
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(
            asset, 'Primary', variantLabels, variantConfig)
        if len(object_list) == 0:
            return
        env_map = object_list[0]

        # extract resolution
        resolution = 4 * 1000

        if len(env_map['variants']) > 0:
            if 'Resolution' in env_map['variants'][0]:
                res_str = env_map['variants'][0]['Resolution']
                if re.match("^[0-9]+[kK]$", res_str):
                    resolution = int(res_str[:-1]) * 1000
                if re.match("^[0-9]+$", res_str):
                    resolution = int(res_str)

        # name prefix

        asset_name = asset['uid']
        path_to_asset = env_map["file"]["path"]
        asset_name = asset_name.split(".")[1]
        renderer_setup = "mantra"
        create_dome(asset_name,path_to_asset,renderer_setup)
