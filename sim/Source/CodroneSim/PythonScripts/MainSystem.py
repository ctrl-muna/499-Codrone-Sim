import unreal

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
for asset in asset_registry.get_all_assets():
    print(asset.get_full_name())