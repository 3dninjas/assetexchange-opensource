#if UNITY_EDITOR

namespace AssetExchange
{
    using AssetExchange.LightJSON;
    using UnityEngine;

    public class AssetPushServiceV1
    {
        public JsonValue SupportedTypes(JsonValue _)
        {
            return new JsonArray(
                "environment.hdri",
                "mesh+surface.maps",
                "surface.maps"
            );
        }

        public JsonValue PushAllowed(JsonValue _)
        {
            return true;
        }

        [MainThread]
        public JsonValue Push(JsonValue data)
        {
            if (data["asset"]["typeUid"] == "environment.hdri")
            {
                Importer.EnvironmentHDRI.Import(data["asset"], data["selectedVariants"]);
                return true;
            }

            if (data["asset"]["typeUid"] == "surface.maps")
            {
                Importer.SurfaceMaps.Import(data["asset"], data["selectedVariants"]);
                return true;
            }

            return false;
        }
    }
}

#endif
