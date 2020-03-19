import re

import assetexchange_shared


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
        name = asset['uid'].replace(".", "_") + "_" + "_".join(variantConfig)
        print name
        # create texture
        #env_tex_node = maya.cmds.shadingNode(
        #    'file', asTexture=True, name=(name + "_env_tex"))
        #maya.cmds.setAttr(env_tex_node+".ftn",
        #                  env_map["file"]["path"], type="string")
        #maya.cmds.setAttr(env_tex_node+".cs", "Raw", type="string")

        # create skydome
        #env_skydome_node = mtoa.utils.createLocator(
        #    "aiSkyDomeLight", asLight=True)
        #maya.cmds.setAttr(env_skydome_node[0]+".resolution", resolution)
        #maya.cmds.connectAttr(env_tex_node+".outColor",
        #                      env_skydome_node[0] + ".color")
