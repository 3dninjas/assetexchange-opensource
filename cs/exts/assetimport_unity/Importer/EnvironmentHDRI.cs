#if UNITY_EDITOR

namespace AssetExchange.Importer
{
    using System;
    using System.IO;
    using System.Linq;
    using AssetExchange.LightJSON;
    using UnityEditor;
    using UnityEngine;

    public static class EnvironmentHDRI
    {
        public static void Import(JsonObject asset, JsonObject selectedVariants)
        {
            // explode variants
            var (variantLabels, variantConfigs) = AssetUtils.VariantUtil.Explode("Primary", selectedVariants);

            // iterate variant config
            foreach (var variantConfig in variantConfigs)
            {
                // get environment map
                var objectList = AssetUtils.VariantUtil.FilterObjectsByVariantConfig(asset, "Primary", variantLabels, variantConfig);
                if (objectList.Count == 0)
                    return;
                var envMap = objectList[0];

                // target paths
                var relTargetPath = "Assets/Import/" + asset["sourceUid"].AsString;
                var targetPath = Path.Combine(Application.dataPath, "Import", asset["sourceUid"].AsString);

                Directory.CreateDirectory(targetPath);

                // find free name
                var texName = AssetUtils.PathUtil.FreeDirEntryName(
                    targetPath,
                    asset["assetId"].AsString.Replace('.', '_') + "_" + string.Join("_", variantConfig.Select(i => i.AsString)),
                    Path.GetExtension(envMap["file"]["path"])
                );

                // import equirectangular hdri
                File.Copy(envMap["file"]["path"], Path.Combine(targetPath, texName));
                AssetDatabase.Refresh();

                // convert to cubemap
                TextureImporter importer = (TextureImporter)AssetImporter.GetAtPath(relTargetPath + "/" + texName);
                importer.maxTextureSize = 8192;
                importer.textureShape = TextureImporterShape.TextureCube;
                importer.SaveAndReimport();

                // load cubemap
                var cubemap = (Cubemap)AssetDatabase.LoadAssetAtPath(relTargetPath + "/" + texName, typeof(Cubemap));
                if (cubemap == null)
                {
                    throw new Exception("Could not load " + texName);
                }

                // create material
                var matName = Path.GetFileNameWithoutExtension(texName) + ".mat";
                var mat = new Material(Shader.Find("Skybox/Cubemap"));
                mat.SetTexture("_Tex", cubemap);
                AssetDatabase.CreateAsset(mat, relTargetPath + "/" + matName);

                // activate environment map
                RenderSettings.skybox = mat;
            }
        }
    }

}

#endif
