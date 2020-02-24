import c4d
import assetexchange_shared

def create_redshift_environment(doc, name, filepath):
    rs_domelight = c4d.BaseObject(1036751)
    rs_domelight.SetName(name)
    rs_domelight[c4d.REDSHIFT_LIGHT_TYPE] = 4
    rs_domelight[c4d.REDSHIFT_LIGHT_DOME_TEX0, c4d.REDSHIFT_FILE_PATH] = str(filepath)

    doc.StartUndo()

    doc.InsertObject(rs_domelight)
    doc.AddUndo(c4d.UNDOTYPE_NEW, rs_domelight)

    doc.EndUndo()
    c4d.EventAdd()

def environment_hdri_redshift(doc, asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:
        # get environment map
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        if len(object_list) == 0:
            return
        env_map = object_list[0]

        name = asset['uid'] + "_" + "_".join(variantConfig)
        filepath = env_map["file"]["path"]
        create_redshift_environment(doc, name, filepath)
