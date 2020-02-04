import os
import errno


def environment_name():
    return os.getenv('ASSETNINJA_ENVIRONMENT', 'primary')


def runtime_path(*parts):
    path = os.path.join(os.path.expanduser("~"), ".assetninja", *parts)
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return path


def environment_path(*parts):
    return runtime_path(environment_name(), *parts)


def registry_root_path(*parts):
    return environment_path('registry', *parts)
