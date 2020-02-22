import itertools


def explode_variants(assemblyName, variants):
    if assemblyName not in variants:
        return ([], [])
    # build cartesian product out of provided variants
    labels = list(variants[assemblyName].keys())
    configs = itertools.product(*list(variants[assemblyName].values()))
    return (labels, configs)


def filter_objects_by_variant_config(asset, assemblyName, variantLabels, variantConfig):
    if assemblyName not in asset['assemblies']:
        return []

    def filter_by_config(obj):
        for obj_variant in obj['variants']:
            matches = True
            for idx, label in enumerate(variantLabels):
                if variantConfig[idx] != obj_variant[label]:
                    matches = False
            if matches:
                return True
        return False
    return list(filter(filter_by_config, list(asset['assemblies'][assemblyName]['objects'].values())))
