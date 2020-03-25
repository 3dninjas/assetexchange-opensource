#if UNITY_EDITOR

namespace AssetExchange.AssetUtils
{
    using System.Collections.Generic;
    using System.Linq;
    using AssetExchange.LightJSON;

    public static class VariantUtil
    {
        public static (IList<string>, IList<IList<JsonValue>>) Explode(string assemblyName, JsonObject variants)
        {
            variants = variants[assemblyName];

            var labels = from KeyValuePair<string, JsonValue> v in variants select v.Key;
            var values = from JsonValue v in variants select (IEnumerable<JsonValue>)v.AsJsonArray;

            var configs = values.Aggregate(
                (IEnumerable<IEnumerable<JsonValue>>)new[] { Enumerable.Empty<JsonValue>() },
                (accumulator, sequence) =>
                    from accseq in accumulator
                    from item in sequence
                    select accseq.Concat(new[] { item }));

            return (labels.ToList(), configs.Select(x => (IList<JsonValue>)x.ToList()).ToList());
        }

        public static IList<JsonObject> FilterObjectsByVariantConfig(JsonObject asset, string assemblyName, IList<string> variantLabels, IList<JsonValue> variantConfig)
        {
            var assemblies = asset["assemblies"].AsJsonObject;

            if (!assemblies.ContainsKey(assemblyName))
            {
                return new JsonObject[] { };
            }

            var objects = from JsonValue obj in assemblies[assemblyName]["objects"].AsJsonObject select obj.AsJsonObject;

            bool filterByConfig(JsonObject obj)
            {
                foreach (JsonObject objVariant in obj["variants"].AsJsonArray)
                {
                    var matches = true;
                    for (int idx = 0; idx < variantLabels.Count; ++idx)
                    {
                        var label = variantLabels[idx];
                        if (variantConfig[idx] != objVariant[label])
                        {
                            matches = false;
                        }
                    }
                    if (matches)
                    {
                        return true;
                    }
                }

                return false;
            }

            return (from obj in objects where filterByConfig(obj) select obj).ToList();
        }
    }
}

#endif
