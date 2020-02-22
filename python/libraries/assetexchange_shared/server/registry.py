import os
from .. import common


def registration_path(category, type):
    return os.path.join(common.registry_root_path(category, type), str(os.getpid()))
