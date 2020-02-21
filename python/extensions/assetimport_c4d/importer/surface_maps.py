import c4d
import assetexchange_shared

def _bmp_shader(doc, filepath='', channel=c4d.MATERIAL_LUMINANCE_SHADER, material=None):
    shader = c4d.BaseList2D(c4d.Xbitmap)
    material[channel] = shader

    shader[c4d.BITMAPSHADER_FILENAME] = str(filepath)

    material.InsertShader(shader)
    doc.AddUndo(c4d.UNDOTYPE_NEW, shader)

def CreateMaterial(doc, mat_name, surface_maps):
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    mat.SetName(mat_name)

    # add diffuse
    if "Diffuse" in surface_maps:
        mat[c4d.MATERIAL_USE_COLOR] = True
        _bmp_shader(doc, surface_maps["Diffuse"]["file"]["path"], c4d.MATERIAL_COLOR_SHADER, mat)

    # add specular
    if "Specular" in surface_maps:
        mat[c4d.MATERIAL_USE_REFLECTION] = True
        _bmp_shader(doc, surface_maps["Specular"]["file"]["path"], c4d.REFLECTION_LAYER_COLOR_TEXTURE, mat)

    # # add roughness
    # if "Roughness" in surface_maps:
    #     mat[c4d.MATERIAL_USE_REFLECTION] = True
    #     _bmp_shader(doc, surface_maps["Roughness"]["file"]["path"], c4d.REFLECTION_LAYER_COLOR_TEXTURE, mat)

    # add normal
    if "Normal" in surface_maps:
        mat[c4d.MATERIAL_USE_NORMAL] = True
        _bmp_shader(doc, surface_maps["Normal"]["file"]["path"], c4d.MATERIAL_NORMAL_SHADER, mat)

    # add displacement
    if "Displacement" in surface_maps:
        # displacement node
        mat[c4d.MATERIAL_USE_DISPLACEMENT] = True
        _bmp_shader(doc, surface_maps["Displacement"]["file"]["path"], c4d.MATERIAL_DISPLACEMENT_SHADER, mat)
        mat[c4d.MATERIAL_DISPLACEMENT_STRENGTH] = 0.1

    doc.InsertMaterial(mat)
    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
    mat.Message(c4d.MSG_UPDATE)

def surface_maps(doc, asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get all maps and convert to dictionary by map type
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        surface_maps = {surface_map["type"]: surface_map for surface_map in object_list}

        # create material object
        mat_name = asset['uid'] + "_" + "_".join(variantConfig)
        CreateMaterial(doc, mat_name, surface_maps)
