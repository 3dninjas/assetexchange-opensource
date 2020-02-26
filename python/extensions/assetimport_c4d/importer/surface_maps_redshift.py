import c4d
import assetexchange_shared
from .RedshiftWrapper import Redshift

def Create_Redshift_Material(doc, mat_name, surface_maps):
    rs = Redshift()
    if rs is False:
        print "Redshift Wrapper not working..."
        return False

    mat = rs.CreateMaterial()
    rs.SetMat(mat)
    mat.SetName(mat_name)

    listNode = rs.GetAllNodes()

    MatNode = None
    OutPutNode = None
    for node in listNode:
        if node.GetType() == "Output": OutPutNode = node
        elif node.GetType() == "Material": MatNode = node

    MatNode[c4d.REDSHIFT_SHADER_MATERIAL_REFL_FRESNEL_MODE] = 1

    # add diffuse
    if "Diffuse" in surface_maps:
        diffuse_or_albedo = surface_maps["Diffuse"]["file"]["path"]

        if "Albedo" in surface_maps:
            diffuse_or_albedo = surface_maps["Albedo"]["file"]["path"]

        MatNode.ExposeParameter(c4d.REDSHIFT_SHADER_MATERIAL_DIFFUSE_COLOR, c4d.GV_PORT_INPUT)
        texNodeCol = rs.CreateShader("TextureSampler", x=-100, y=200)
        texNodeCol.SetName('Diffuse')
        texNodeCol[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0, c4d.REDSHIFT_FILE_PATH] = str(diffuse_or_albedo)
        rs.CreateConnection(texNodeCol, MatNode, 0, 0)

    # add roughness
    if 'Roughness' in surface_maps:
        MatNode.ExposeParameter(c4d.REDSHIFT_SHADER_MATERIAL_REFL_ROUGHNESS, c4d.GV_PORT_INPUT)
        filepath = surface_maps["Roughness"]["file"]["path"]
        TexNodeGloss=rs.CreateShader("TextureSampler", x=-500, y=300)
        TexNodeGloss.SetName('Roughness')
        TexNodeGloss[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0, c4d.REDSHIFT_FILE_PATH] = str(filepath)
        TexNodeGloss[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0_GAMMAOVERRIDE] = 1

        invert = rs.CreateShader("RSMathInv", x=-300, y=300)
        rs.CreateConnection(invert, MatNode, 0, 1)
        invert.ExposeParameter(c4d.REDSHIFT_SHADER_RSMATHINV_INPUT, c4d.GV_PORT_INPUT)
        rs.CreateConnection(TexNodeGloss, invert, 0, 0)

    # add specular
    if 'Specular' in surface_maps:
        MatNode.ExposeParameter(c4d.REDSHIFT_SHADER_MATERIAL_REFL_REFLECTIVITY, c4d.GV_PORT_INPUT)
        filepath = surface_maps["Roughness"]["file"]["path"]
        TexNodeMetal=rs.CreateShader("TextureSampler", x=-100, y=400)
        TexNodeMetal.SetName('Specular')
        TexNodeMetal[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0, c4d.REDSHIFT_FILE_PATH] = str(filepath)
        #TexNodeMetal[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0_GAMMAOVERRIDE] = 1
        rs.CreateConnection(TexNodeMetal, MatNode, 0, 2)

    # add normal
    if 'Normal' in surface_maps:
        MatNode.ExposeParameter(c4d.REDSHIFT_SHADER_MATERIAL_BUMP_INPUT, c4d.GV_PORT_INPUT)
        filepath = surface_maps["Normal"]["file"]["path"]
        BumpNode = rs.CreateShader("BumpMap", x=-50, y=500)
        BumpNode[c4d.REDSHIFT_SHADER_BUMPMAP_INPUTTYPE] = 1
        BumpNode.ExposeParameter(c4d.REDSHIFT_SHADER_BUMPMAP_INPUT, c4d.GV_PORT_INPUT)

        TexNodeNorm = rs.CreateShader("TextureSampler", x=-200, y=500)
        TexNodeNorm.SetName('NormalMap')
        TexNodeNorm[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0, c4d.REDSHIFT_FILE_PATH] = str(filepath)
        TexNodeNorm[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0_GAMMAOVERRIDE] = 1
        rs.CreateConnection(TexNodeNorm, BumpNode, 0, 0)

        rs.CreateConnection(BumpNode, MatNode, 0, "Bump Input")

    # add displacement
    if "Displacement" in surface_maps:
        OutPutNode.ExposeParameter(c4d.GV_REDSHIFT_OUTPUT_DISPLACEMENT, c4d.GV_PORT_INPUT)
        filepath = surface_maps["Displacement"]["file"]["path"]
        DisplNode = rs.CreateShader("Displacement", x=-50, y=600)
        DisplNode.SetName('Displacement')
        DisplNode.ExposeParameter(c4d.REDSHIFT_SHADER_DISPLACEMENT_TEXMAP, c4d.GV_PORT_INPUT)

        TexNodeDispl = rs.CreateShader("TextureSampler", x=-250, y=600)
        TexNodeDispl.SetName('Displacement')
        TexNodeDispl[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0, c4d.REDSHIFT_FILE_PATH] = str(filepath)
        rs.CreateConnection(TexNodeDispl, DisplNode, 0, 0)

        rs.CreateConnection(DisplNode, OutPutNode, 0, "Displacement")


    # if 'EmissiveColor' in textures:
    #     texEmit = textures['EmissiveColor'] #r"H:\01_Projects\Daniel_Projects\3DC-C4D_Workflow\Export_to_C4D\Can01_default_color.png"
    #     texNodeEmit=rs.CreateShader("TextureSampler", x=-300, y=200)
    #     texNodeEmit.SetName('Tex Emission')
    #     texNodeEmit[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0, c4d.REDSHIFT_FILE_PATH]=texEmit

def surface_maps_redshift(doc, asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get all maps and convert to dictionary by map type
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        surface_maps = {surface_map["type"]: surface_map for surface_map in object_list}

        # name prefix
        # mat_name = asset['uid'].replace(".", "_") + "_" + "_".join(variantConfig)
        mat_name = asset['uid'] + "_" + "_".join(variantConfig)
        Create_Redshift_Material(doc, mat_name, surface_maps)
