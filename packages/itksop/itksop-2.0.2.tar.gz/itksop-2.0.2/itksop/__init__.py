import sys
import os
cwd = os.getcwd()

import importlib
import pkgutil

# from: https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    print("In package:",package)
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        #print(full_name)
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results

# running from X.__init__.py
print('running in:',__name__)
returning=import_submodules(__name__)
#print("\nresults:",returning)
__all__={}
for k,v in returning.items():
    pageName=[x for x in v.__dir__() if x[0:2]!="__" ][-1]
    try:
        print("module name:",getattr(v,pageName)().name)
        #print("module name:",getattr(v,k)().name)
        try:
            __all__[k.split('.')[1]].append(getattr(v,pageName))
        except KeyError:
            __all__[k.split('.')[1]] = [getattr(v,pageName)]
    except AttributeError and TypeError:
        pass

print(__all__)
