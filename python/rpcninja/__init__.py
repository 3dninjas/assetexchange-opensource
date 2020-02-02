import importlib

from . import shared
if importlib.util.find_spec("bpy") is not None:
    from . import blender
