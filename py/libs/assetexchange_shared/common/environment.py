import os
import errno


def lookup_assetexchange_path(*parts):
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
    path = os.path.join(path, ".assetexchange", *parts)
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return path


def services_path(*parts):
    return lookup_assetexchange_path('services', *parts)
