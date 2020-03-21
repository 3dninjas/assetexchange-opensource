import assetexchange_shared
import os
import ix


def create_dome(name,path_to_hdri_map):
    ix.log_info("Creating HDRI Dome, you can Undo.")
    create_env = None
    ix.begin_command_batch("AssetNinjaImportHdri")
    clean_name = str(name)
    mapfile = ix.cmds.CreateObject(clean_name, 'TextureMapFile')
    mapfile.attrs.projection = 5
    path_to_hdri_map = str(path_to_hdri_map)
    mapfile.attrs.filename = path_to_hdri_map
    mapfile.attrs.interpolation_mode = 1
    mapfile.attrs.mipmap_filtering_mode = 1
    mapfile.attrs.color_space_auto_detect = False
    mapfile.attrs.file_color_space = 'linear'
    mapfile.attrs.pre_multiplied = False
    ibl_name = "IBL_"+clean_name
    light = ix.cmds.CreateObject(ibl_name, 'LightPhysicalEnvironment')
    ix.cmds.SetTexture([light.get_full_name() + ".color"], mapfile.get_full_name())
    if create_env:
        env = ix.cmds.CreateObject('ibl_env', 'GeometrySphere')
        env_mat = ix.cmds.CreateObject('ibl_mat', 'MaterialMatte')
        env.attrs.override_material = env_mat
        env.attrs.unseen_by_camera = True
        env.attrs.cast_shadows = False
        env.attrs.receive_shadows = False
        env.attrs.is_emitter = False
        env.attrs.radius = 500001
        env.attrs.unseen_by_rays = True
        env.attrs.unseen_by_reflections = True
        env.attrs.unseen_by_refractions = True
        env.attrs.unseen_by_gi = True
        env.attrs.unseen_by_sss = True
        ix.cmds.SetTexture([env_mat.get_full_name() + ".color"], mapfile.get_full_name())
        ix.cmds.SetTexture([light.get_full_name() + ".parent"], env.get_full_name())

    ix.end_command_batch()
    ix.log_info("Dome IBL Done.")

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

        # clarisse run import
        ix.log_info("Ninja works. Does iFX stuff.")
        asset_name = asset['uid']
        path_to_asset = env_map["file"]["path"]
        asset_name = asset_name.split(".")[1]
        #print asset_name
        create_dome(asset_name,path_to_asset)
        ix.log_info("Run done.")
