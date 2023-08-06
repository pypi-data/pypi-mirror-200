from os import getenv, getpid, listdir
from os.path import join
from subprocess import check_call, DEVNULL, check_output
from sys import path
from traceback import print_exc

if eclipse := getenv('PYDEVD'):
    try:
        plugins = join(eclipse, 'plugins')

        def pydev():
            prefix = 'org.python.pydev.core_'
            if version := getenv('PYDEVD_VERSION'):
                return prefix + version
            else:
                for plugin in listdir(plugins):
                    if plugin.startswith(prefix):
                        return plugin
            raise Exception(f'PyDev not found at {plugins}/{prefix}*')

        port = getenv('PYDEVD_PORT', default=5678)
        try:
            check_call(f'nc -vz localhost {port}'.split(), stderr=DEVNULL)
            try:
                process = f'ps -p {getpid()} -o args='.split()
                if 'pydevd.py' not in check_output(process).decode('utf-8'):
                    path.append(join(plugins, pydev(), 'pysrc'))
                    __import__("pydevd").settrace()
                    print('Remote debugging ready. Press F8 or F6 to start')
            except:
                print_exc()
        except:
            pass
    except:
        print_exc()