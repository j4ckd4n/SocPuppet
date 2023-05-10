import os
import importlib.util

directory = os.path.dirname(__file__)
package_name = "your_package_name"

for module_file in os.listdir(directory):
  module_name, ext = os.path.splitext(module_file)

  if ext == ".py" and module_name != "__init__":
    module_path = os.path.join(directory, module_file)

    spec = importlib.util.spec_from_file_location(f"{package_name}.{module_name}", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
