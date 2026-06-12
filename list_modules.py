import pkgutil
import nubra_python_sdk

for module in pkgutil.walk_packages(
    nubra_python_sdk.__path__,
    nubra_python_sdk.__name__ + "."
):
    print(module.name)