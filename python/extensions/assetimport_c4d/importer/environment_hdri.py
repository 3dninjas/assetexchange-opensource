import c4d
import assetexchange_shared

def _bmp_shader(doc, filepath='', channel=c4d.MATERIAL_LUMINANCE_SHADER, material=None):
    shader = c4d.BaseList2D(c4d.Xbitmap)
    material[channel] = shader

    shader[c4d.BITMAPSHADER_FILENAME] = filepath

    material.InsertShader(shader)
    doc.AddUndo(c4d.UNDOTYPE_NEW, shader)

def create_standard_environment(doc, name, filepath):
    doc.StartUndo()
    # Create our Material for Sky Object
    mat = c4d.BaseMaterial(c4d.Mmaterial)

    mat.SetName(name)

    mat[c4d.MATERIAL_USE_COLOR] = False
    mat[c4d.MATERIAL_USE_LUMINANCE] = True
    mat[c4d.MATERIAL_USE_REFLECTION] = False

    _bmp_shader(doc, filepath, c4d.MATERIAL_LUMINANCE_SHADER, mat)
    doc.InsertMaterial(mat)
    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)

    # mat.Message(c4d.MSG_UPDATE)
    # mat.Update(True, True)

    # Create Sky Object
    sky = c4d.BaseObject(c4d.Osky)
    sky.SetName(name)
    doc.InsertObject(sky)
    doc.AddUndo(c4d.UNDOTYPE_NEW, sky)

    # Create Texture Tag and set our Material
    tag = c4d.BaseTag(c4d.Ttexture)
    sky.InsertTag(tag)
    tag.SetMaterial(mat)
    doc.AddUndo(c4d.UNDOTYPE_NEW, tag)

    doc.EndUndo()
    c4d.EventAdd()

def environment_hdri(doc, asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:
        # get environment map
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        if len(object_list) == 0:
            return
        env_map = object_list[0]

        name = str(env_map["file"]["name"])
        filepath = str(env_map["file"]["path"])

        create_standard_environment(doc, name, filepath)
