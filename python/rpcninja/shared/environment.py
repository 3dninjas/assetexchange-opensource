import os


def environment_name():
    return os.getenv('ASSETNINJA_ENVIRONMENT', 'primary')


def runtime_dir(*parts):
    path = os.path.join(os.path.expanduser("~"), ".assetninja", *parts)
    os.makedirs(path, exist_ok=True)
    return path


def environment_dir(*parts):
    return runtime_dir(environment_name(), *parts)


def registry_root_dir(*parts):
    return environment_dir('registry', *parts)
