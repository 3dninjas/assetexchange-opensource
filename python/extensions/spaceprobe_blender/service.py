import assetexchange_blender
import addon_utils
import bpy


class SpaceProbeService:
    # eval code
    @assetexchange_blender.execute_on_main_thread
    def Eval(self, code):
        return eval(code)

    # refresh addons
    @assetexchange_blender.execute_on_main_thread
    def RefreshAddons(self, _):
        addon_utils.modules_refresh()
        return True

    # list addons
    @assetexchange_blender.execute_on_main_thread
    def ListAddons(self, _):
        user_scripts_path = bpy.utils.user_resource('SCRIPTS')
        return {v.__name__: {
            'is_enabled': addon_utils.check(v.__name__)[0],
            'is_loaded': addon_utils.check(v.__name__)[1],
            'is_user_addon': v.__file__.startswith(user_scripts_path),
            'path': v.__file__ if not v.__file__.endswith('/__init__.py') else v.__file__[:-11],
            'info': v.bl_info
        } for v in addon_utils.modules()}

    # enable addon
    @assetexchange_blender.execute_on_main_thread
    def EnableAddon(self, addon_name):
        addon_utils.enable(addon_name, default_set=True, persistent=True)
        addon_utils.modules_refresh()
        return {
            'is_enabled': addon_utils.check(addon_name)[0],
            'is_loaded': addon_utils.check(addon_name)[1],
        }

    # disable addon
    @assetexchange_blender.execute_on_main_thread
    def DisableAddon(self, addon_name):
        addon_utils.disable(addon_name, default_set=True)
        addon_utils.modules_refresh()
        return {
            'is_enabled': addon_utils.check(addon_name)[0],
            'is_loaded': addon_utils.check(addon_name)[1],
        }
