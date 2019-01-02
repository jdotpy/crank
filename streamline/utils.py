from importlib import import_module
import sys
import os

def get_file_io(name, write=False):
    # Test for file-like objects we can use first
    if hasattr(name, 'write') and write:
        return name
    elif hasattr(name, 'read') and not write:
        return name

    # Test for stdin/stdout special case
    if name == '-' and write:
        return sys.stdout
    elif name == '-' and not write:
        return sys.stdin

    # Assume this is a file
    return open(name, 'w' if write else 'r', 1)

def import_obj(path):
    # Ensure the current directory is on the path
    current_dir = os.path.abspath('.')
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    # Split the object name and the module path
    module_path, handler_name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, handler_name)
    for attr in module_path.split('.')[1:]:
        module = getattr(module, attr)
    handler_obj = getattr(module, handler_name)
    if handler_obj is None:
        raise ValueError('Unable to import object: {}'.format(path))
    return handler_obj

def inject_module(module_name, namespace):
    try:
        module = import_module(module_name)
    except ModuleNotFoundError as e:
        print('This plugin requires module: "{}"\nTry "pip install {}"'.format(module_name, module_name))
        sys.exit(6)
    sys.modules[module_name] = module
    namespace[module_name] = module

def truthy(entries):
    return [entry for entry in entries if entry]
