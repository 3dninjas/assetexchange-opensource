import c4d
import assetexchange_shared

def _insert_shader(doc, filepath='', channel=c4d.MATERIAL_LUMINANCE_SHADER, material=None):
    shader = c4d.BaseList2D(c4d.Xbitmap)
    material[channel] = shader

    shader[c4d.BITMAPSHADER_FILENAME] = str(filepath)

    material.InsertShader(shader)
    doc.AddUndo(c4d.UNDOTYPE_NEW, shader)

# def Create_Standard_Material(doc, mat_name, surface_maps):
#     mat = c4d.BaseMaterial(c4d.Mmaterial)
#     mat.SetName(mat_name)
#
#     # add diffuse
#     if "Diffuse" in surface_maps:
#         mat[c4d.MATERIAL_USE_COLOR] = True
#         _insert_shader(doc, surface_maps["Diffuse"]["file"]["path"], c4d.MATERIAL_COLOR_SHADER, mat)
#
#     # add specular
#     if "Specular" in surface_maps:
#         mat[c4d.MATERIAL_USE_REFLECTION] = True
#         _insert_shader(doc, surface_maps["Specular"]["file"]["path"], c4d.REFLECTION_LAYER_COLOR_TEXTURE, mat)
#
#     # # add roughness
#     # if "Roughness" in surface_maps:
#     #     mat[c4d.MATERIAL_USE_REFLECTION] = True
#     #     _insert_shader(doc, surface_maps["Roughness"]["file"]["path"], c4d.REFLECTION_LAYER_COLOR_TEXTURE, mat)
#
#     # add normal
#     if "Normal" in surface_maps:
#         mat[c4d.MATERIAL_USE_NORMAL] = True
#         _insert_shader(doc, surface_maps["Normal"]["file"]["path"], c4d.MATERIAL_NORMAL_SHADER, mat)
#
#     # add displacement
#     if "Displacement" in surface_maps:
#         # displacement node
#         mat[c4d.MATERIAL_USE_DISPLACEMENT] = True
#         _insert_shader(doc, surface_maps["Displacement"]["file"]["path"], c4d.MATERIAL_DISPLACEMENT_SHADER, mat)
#         mat[c4d.MATERIAL_DISPLACEMENT_STRENGTH] = 0.1
#
#     doc.InsertMaterial(mat)
#     doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
#     # mat.Message(c4d.MSG_UPDATE)

def Create_PBR_Material(doc, mat_name, surface_maps):
    doc.StartUndo()

    mat = c4d.Material(c4d.Mmaterial)
    mat.SetName(mat_name)

    mat.RemoveReflectionAllLayers()
    mat.SetChannelState(c4d.CHANNEL_COLOR, False)
    mat.SetChannelState(c4d.CHANNEL_REFLECTION, True)

    # GENERAL: YOU HAVE TO ADD THE ID of the Reflection Layer to each FLAG_ID ! -> dID & sID
    # add diffuse
    if "Diffuse" in surface_maps:
        # Lambertian Diffuse
        diffuse = mat.AddReflectionLayer()
        diffuse.SetName('Default Diffuse')
        dID = diffuse.GetDataID()
        mat[c4d.REFLECTION_LAYER_MAIN_DISTRIBUTION + dID] = c4d.REFLECTION_DISTRIBUTION_LAMBERTIAN
        mat[c4d.REFLECTION_LAYER_MAIN_VALUE_SPECULAR + dID] = 1.0
        #Insert Diffuse
        _insert_shader(doc, surface_maps["Diffuse"]["file"]["path"], c4d.REFLECTION_LAYER_COLOR_TEXTURE + dID, mat)

    # add roughness
    if "Roughness" in surface_maps:
        # Beckmann Reflection
        specular = mat.AddReflectionLayer()
        specular.SetName('Default Reflection')
        sID = specular.GetDataID()
        mat[c4d.REFLECTION_LAYER_MAIN_DISTRIBUTION+ sID] = c4d.REFLECTION_DISTRIBUTION_BECKMANN

        #Insert Roughness
        _insert_shader(doc, surface_maps["Roughness"]["file"]["path"], c4d.REFLECTION_LAYER_MAIN_SHADER_ROUGHNESS + sID, mat)
        mat[c4d.REFLECTION_LAYER_MAIN_VALUE_ROUGHNESS + sID] = 0.3
        mat[c4d.REFLECTION_LAYER_MAIN_VALUE_SPECULAR + sID] = 1.0

        # REFLECTION_FRESNEL_DIELECTRIC
        mat[c4d.REFLECTION_LAYER_FRESNEL_MODE + sID] = c4d.REFLECTION_FRESNEL_DIELECTRIC

    # add normal
    if "Normal" in surface_maps:
        mat[c4d.MATERIAL_USE_NORMAL] = True
        #Flip X (Red)
        mat[c4d.MATERIAL_NORMAL_REVERSEX] = True
        _insert_shader(doc, surface_maps["Normal"]["file"]["path"], c4d.MATERIAL_NORMAL_SHADER, mat)

    # add displacement
    if "Displacement" in surface_maps:
        # displacement node
        mat[c4d.MATERIAL_USE_DISPLACEMENT] = True
        _insert_shader(doc, surface_maps["Displacement"]["file"]["path"], c4d.MATERIAL_DISPLACEMENT_SHADER, mat)
        mat[c4d.MATERIAL_DISPLACEMENT_STRENGTH] = 0.1

    # Let's make the Material Preview a little prettier
    mat[c4d.MATERIAL_PREVIEWSIZE] = c4d.MATERIAL_PREVIEWSIZE_512

    doc.InsertMaterial(mat)
    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)

    doc.EndUndo()
    c4d.EventAdd()

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
        Create_PBR_Material(doc, mat_name, surface_maps)
