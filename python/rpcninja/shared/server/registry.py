import os
from .. import environment


def registration_path(category, type):
    return os.path.join(environment.registry_root_path(category, type), str(os.getpid()))
