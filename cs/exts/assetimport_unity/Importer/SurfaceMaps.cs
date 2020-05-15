#if UNITY_EDITOR

namespace AssetExchange.Importer
{
    using System;
    using System.IO;
    using System.Linq;
    using AssetExchange.LightJSON;
    using UnityEditor;
    using UnityEngine;

    public static class SurfaceMaps
    {
        public static Texture2D MergeTextures(Texture2D texRgb, Color defRgb, Texture2D texAlpha, float defAlpha, bool invertAlpha)
        {
            if (texRgb == null && texAlpha == null)
            {
                throw new Exception("cannot merge two unknown textures");
            }

            var width = texRgb != null ? texRgb.width : texAlpha.width;
            var height = texRgb != null ? texRgb.height : texAlpha.height;

            Color[] pixRgb = texRgb != null ? texRgb.GetPixels() : null;
            Color[] pixAlpha = texAlpha != null ? texAlpha.GetPixels() : null;

            Color[] pix = new Color[width * height];

            for (int i = 0; i < width * height; ++i)
            {
                pix[i] = pixRgb != null ? pixRgb[i] : defRgb;
                pix[i].a = pixAlpha != null ? ((pixAlpha[i].r + pixAlpha[i].g + pixAlpha[i].b) / 3.0f) : defAlpha;
                pix[i].a = invertAlpha ? 1.0f - pix[i].a : pix[i].a;
            }

            Texture2D tex = new Texture2D(width, height, TextureFormat.RGBAFloat, false);
            tex.SetPixels(pix);

            return tex;
        }

        public static Texture2D InvertNormapMap(Texture2D texIn)
        {
            if (texIn == null)
            {
                throw new Exception("input map not provided");
            }

            var width = texIn.width;
            var height = texIn.height;

            Color[] pixIn = texIn.GetPixels();
            Color[] pixOut = new Color[width * height];

            for (int i = 0; i < width * height; ++i)
            {
                pixOut[i] = pixIn[i];
                pixOut[i].g = 1.0f - pixOut[i].g;
            }

            Texture2D texOut = new Texture2D(width, height, TextureFormat.RGB24, false);
            texOut.SetPixels(pixOut);

            return texOut;
        }

        public static void Import(JsonObject asset, JsonObject selectedVariants)
        {
            // explode variants
            var (variantLabels, variantConfigs) = AssetUtils.VariantUtil.Explode("Primary", selectedVariants);

            // iterate variant config
            foreach (var variantConfig in variantConfigs)
            {
                // get all maps and convert to dictionary by map type
                var objectList = AssetUtils.VariantUtil.FilterObjectsByVariantConfig(asset, "Primary", variantLabels, variantConfig);
                var surfaceMaps = objectList.ToDictionary(surfaceMap => surfaceMap["type"].AsString);

                // target paths
                var relTargetPath = "Assets/Import/" + asset["sourceUid"].AsString;
                var targetPath = Path.Combine(Application.dataPath, "Import", asset["sourceUid"].AsString);

                Directory.CreateDirectory(targetPath);

                // find free name
                var matName = AssetUtils.PathUtil.FreeDirEntryName(
                    targetPath,
                    asset["assetId"].AsString.Replace('.', '_') + "_" + string.Join("_", variantConfig.Select(i => i.AsString)),
                    ".mat"
                );

                // detect workflow
                var isMetalnessRoughnessFlow = surfaceMaps.ContainsKey("Metalness") || !surfaceMaps.ContainsKey("Specular");

                // prepare material
                var mat = new Material(Shader.Find(isMetalnessRoughnessFlow ? "Standard" : "Standard (Specular setup)"));

                // add Diffuse
                if (surfaceMaps.ContainsKey("Base Color") || surfaceMaps.ContainsKey("Albedo") || surfaceMaps.ContainsKey("Diffuse"))
                {
                    // import texture
                    var texSrcPath = (
                        surfaceMaps.ContainsKey("Base Color") ? surfaceMaps["Base Color"] : (
                            surfaceMaps.ContainsKey("Albedo") ? surfaceMaps["Albedo"] : (
                                surfaceMaps["Diffuse"]
                            )
                        )
                    )["file"]["path"];
                    var texName = Path.GetFileNameWithoutExtension(matName) + "_Diffuse" + Path.GetExtension(texSrcPath);
                    File.Copy(texSrcPath, Path.Combine(targetPath, texName));
                    AssetDatabase.Refresh();
                    // fix texture parameter
                    TextureImporter importer = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texName);
                    importer.maxTextureSize = 8192;
                    importer.SaveAndReimport();
                    // link to material
                    var tex = (Texture)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texName, typeof(Texture));
                    mat.SetTexture("_MainTex", tex);
                }

                // add Metalness and/or Roughness
                if (isMetalnessRoughnessFlow && (surfaceMaps.ContainsKey("Metalness") || surfaceMaps.ContainsKey("Roughness")))
                {
                    // import texture
                    string texNameMetalness = null;
                    if (surfaceMaps.ContainsKey("Metalness"))
                    {
                        // copy file
                        var texSrcPath = surfaceMaps["Metalness"]["file"]["path"];
                        texNameMetalness = Path.GetFileNameWithoutExtension(matName) + "_Metalness" + Path.GetExtension(texSrcPath);
                        File.Copy(texSrcPath, Path.Combine(targetPath, texNameMetalness));
                        AssetDatabase.Refresh();
                        // fix texture parameter
                        TextureImporter importerMetalness = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texNameMetalness);
                        importerMetalness.maxTextureSize = 8192;
                        importerMetalness.isReadable = true;
                        importerMetalness.SaveAndReimport();
                    }
                    string texNameRoughness = null;
                    if (surfaceMaps.ContainsKey("Roughness"))
                    {
                        // copy file
                        var texSrcPath = surfaceMaps["Roughness"]["file"]["path"];
                        texNameRoughness = Path.GetFileNameWithoutExtension(matName) + "_Roughness" + Path.GetExtension(texSrcPath);
                        File.Copy(texSrcPath, Path.Combine(targetPath, texNameRoughness));
                        AssetDatabase.Refresh();
                        // fix texture parameter
                        TextureImporter importerRoughness = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texNameRoughness);
                        importerRoughness.maxTextureSize = 8192;
                        importerRoughness.isReadable = true;
                        importerRoughness.SaveAndReimport();
                    }
                    // merge textures
                    var texMetalness = texNameMetalness != null
                        ? (Texture2D)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texNameMetalness, typeof(Texture2D))
                        : null;
                    var texRoughness = texNameRoughness != null
                        ? (Texture2D)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texNameRoughness, typeof(Texture2D))
                        : null;
                    var tex = MergeTextures(texMetalness, new Color(0.0f, 0.0f, 0.0f), texRoughness, 1.0f, true);
                    // delete unmerged textures
                    if (texNameMetalness != null)
                    {
                        AssetDatabase.DeleteAsset(relTargetPath + "/" + texNameMetalness);
                    }
                    if (texNameRoughness != null)
                    {
                        AssetDatabase.DeleteAsset(relTargetPath + "/" + texNameRoughness);
                    }
                    // import merged texture
                    var texName = Path.GetFileNameWithoutExtension(matName) + "_MetalnessGlossiness.png";
                    File.WriteAllBytes(Path.Combine(targetPath, texName), tex.EncodeToPNG());
                    AssetDatabase.Refresh();
                    // fix texture parameter
                    TextureImporter importer = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texName);
                    importer.maxTextureSize = 8192;
                    importer.SaveAndReimport();
                    // link to material
                    var tex2 = (Texture)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texName, typeof(Texture));
                    mat.EnableKeyword ("_METALLICGLOSSMAP");
                    mat.SetTexture("_MetallicGlossMap", tex2);
                }

                // add Specular and/or Roughness
                if (!isMetalnessRoughnessFlow && (surfaceMaps.ContainsKey("Specular") || surfaceMaps.ContainsKey("Roughness")))
                {
                    // import texture
                    string texNameSpecular = null;
                    if (surfaceMaps.ContainsKey("Specular"))
                    {
                        // copy file
                        var texSrcPath = surfaceMaps["Specular"]["file"]["path"];
                        texNameSpecular = Path.GetFileNameWithoutExtension(matName) + "_Specular" + Path.GetExtension(texSrcPath);
                        File.Copy(texSrcPath, Path.Combine(targetPath, texNameSpecular));
                        AssetDatabase.Refresh();
                        // fix texture parameter
                        TextureImporter importerSpecular = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texNameSpecular);
                        importerSpecular.maxTextureSize = 8192;
                        importerSpecular.isReadable = true;
                        importerSpecular.SaveAndReimport();
                    }
                    string texNameRoughness = null;
                    if (surfaceMaps.ContainsKey("Roughness"))
                    {
                        // copy file
                        var texSrcPath = surfaceMaps["Roughness"]["file"]["path"];
                        texNameRoughness = Path.GetFileNameWithoutExtension(matName) + "_Roughness" + Path.GetExtension(texSrcPath);
                        File.Copy(texSrcPath, Path.Combine(targetPath, texNameRoughness));
                        AssetDatabase.Refresh();
                        // fix texture parameter
                        TextureImporter importerRoughness = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texNameRoughness);
                        importerRoughness.maxTextureSize = 8192;
                        importerRoughness.isReadable = true;
                        importerRoughness.SaveAndReimport();
                    }
                    // merge textures
                    var texSpecular = texNameSpecular != null
                        ? (Texture2D)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texNameSpecular, typeof(Texture2D))
                        : null;
                    var texRoughness = texNameRoughness != null
                        ? (Texture2D)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texNameRoughness, typeof(Texture2D))
                        : null;
                    var tex = MergeTextures(texSpecular, new Color(1.0f, 1.0f, 1.0f), texRoughness, 1.0f, true);
                    // delete unmerged textures
                    if (texNameSpecular != null)
                    {
                        AssetDatabase.DeleteAsset(relTargetPath + "/" + texNameSpecular);
                    }
                    if (texNameRoughness != null)
                    {
                        AssetDatabase.DeleteAsset(relTargetPath + "/" + texNameRoughness);
                    }
                    // import merged texture
                    var texName = Path.GetFileNameWithoutExtension(matName) + "_SpecularGlossiness.png";
                    File.WriteAllBytes(Path.Combine(targetPath, texName), tex.EncodeToPNG());
                    AssetDatabase.Refresh();
                    // fix texture parameter
                    TextureImporter importer = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texName);
                    importer.maxTextureSize = 8192;
                    importer.SaveAndReimport();
                    // link to material
                    var tex2 = (Texture)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texName, typeof(Texture));
                    mat.EnableKeyword ("_SPECGLOSSMAP");
                    mat.SetTexture("_SpecGlossMap", tex2);
                }

                // add Normal
                if (surfaceMaps.ContainsKey("Normal"))
                {
                    // import texture
                    var texSrcPath = surfaceMaps["Normal"]["file"]["path"];
                    var texName = Path.GetFileNameWithoutExtension(matName) + "_Normal" + Path.GetExtension(texSrcPath);
                    File.Copy(texSrcPath, Path.Combine(targetPath, texName));
                    AssetDatabase.Refresh();
                    // fix handedness
                    if (surfaceMaps["Normal"]["details"]["handedness"] == "left")
                    {
                        // fix texture parameter
                        TextureImporter importer2 = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texName);
                        importer2.maxTextureSize = 8192;
                        importer2.isReadable = true;
                        importer2.sRGBTexture = false;
                        importer2.SaveAndReimport();
                        // convert normap map
                        var tex2 = InvertNormapMap((Texture2D)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texName, typeof(Texture2D)));
                        // replace normal map
                        AssetDatabase.DeleteAsset(relTargetPath + "/" + texName);
                        texName = Path.GetFileNameWithoutExtension(matName) + "_NormalConverted.png";
                        File.WriteAllBytes(Path.Combine(targetPath, texName), tex2.EncodeToPNG());
                        AssetDatabase.Refresh();
                    }
                    // fix texture parameter
                    TextureImporter importer = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texName);
                    importer.maxTextureSize = 8192;
                    importer.sRGBTexture = false;
                    importer.textureType = TextureImporterType.NormalMap;
                    importer.SaveAndReimport();
                    // link to material
                    var tex = (Texture)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texName, typeof(Texture));
                    mat.EnableKeyword ("_NORMALMAP");
                    mat.SetTexture("_BumpMap", tex);
                }

                // add Displacement
                if (surfaceMaps.ContainsKey("Displacement"))
                {
                    // import texture
                    var texSrcPath = surfaceMaps["Displacement"]["file"]["path"];
                    var texName = Path.GetFileNameWithoutExtension(matName) + "_Displacement" + Path.GetExtension(texSrcPath);
                    File.Copy(texSrcPath, Path.Combine(targetPath, texName));
                    AssetDatabase.Refresh();
                    // fix texture parameter
                    TextureImporter importer = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texName);
                    importer.maxTextureSize = 8192;
                    importer.sRGBTexture = false;
                    importer.SaveAndReimport();
                    // link to material
                    var tex = (Texture)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texName, typeof(Texture));
                    mat.EnableKeyword ("_PARALLAXMAP");
                    mat.SetTexture("_ParallaxMap", tex);
                }

                // create material
                AssetDatabase.CreateAsset(mat, relTargetPath + "/" + matName);
            }
        }
    }

}

#endif
