import assetexchange_shared

def surface_maps(asset, selectedVariants):
    # explode variants
    variantLabels, variantConfigs = assetexchange_shared.asset.explode_variants('Primary', selectedVariants)

    # iterate variant config
    for variantConfig in variantConfigs:

        # get all maps and convert to dictionary by map type
        object_list = assetexchange_shared.asset.filter_objects_by_variant_config(asset, 'Primary', variantLabels, variantConfig)
        surface_maps = {surface_map["type"]: surface_map for surface_map in object_list}

        # create material object
        # TODO

        # add diffuse
        if "Diffuse" in surface_maps:
            # TODO
            pass

        # add specular
        if "Specular" in surface_maps:
            # TODO
            pass

        # add roughness
        if "Roughness" in surface_maps:
            # TODO
            pass

        # add normal
        if "Normal" in surface_maps:
            # TODO
            pass

        # add displacement
        if "Displacement" in surface_maps:
            # TODO
            pass
