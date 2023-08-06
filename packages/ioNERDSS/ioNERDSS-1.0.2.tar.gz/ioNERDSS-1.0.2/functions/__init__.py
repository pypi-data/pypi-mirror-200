import glob
import importlib


# Get a list of all the Python files in the current directory
module_filenames = glob.glob('*.py')

# Import all the modules from the list of filenames
modules = [importlib.import_module('.' + f[:-3], __name__) for f in module_filenames]

# Import all the functions from each module into the package namespace
for module in modules:
    for name in module.__dict__:
        if not name.startswith('_'):
            globals()[name] = module.__dict__[name]