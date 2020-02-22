import os
import errno


def environment_name():
    return os.getenv('ASSETNINJA_ENVIRONMENT', 'primary')


def runtime_path(*parts):
    path = os.path.expanduser("~")
    # workaround required for 2.7, because HOME is checked on windows and sometimes set to Document folder (which is wrong)
    if os.name == 'nt':
        if 'USERPROFILE' in os.environ:
            path = os.environ['USERPROFILE']
        else:
            try:
                drive = os.environ['HOMEDRIVE']
            except KeyError:
                drive = ''
            path = os.path.join(drive, os.environ['HOMEPATH'])
    path = os.path.join(path, ".assetninja", *parts)
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
