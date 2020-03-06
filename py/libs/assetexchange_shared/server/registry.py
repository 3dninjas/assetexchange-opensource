import os
from .. import common


def service_entry_path(category, type):
    return os.path.join(common.services_path(category, type), str(os.getpid()))
