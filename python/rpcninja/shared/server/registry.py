import os
from .. import environment


def extension_registration_file(category, type):
    return os.path.join(environment.registry_root_dir(category, type), str(os.getpid()))
