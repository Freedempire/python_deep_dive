import os.path
import types
import sys

# import module1 manually

module_name = 'module1'
module_file = 'module1_source.py'
module_path = '.'
module_rel_file_path = os.path.join(module_path, module_file)
module_abs_file_path = os.path.abspath(module_rel_file_path)

# read source code from file
with open(module_rel_file_path) as code_file:
    source_code = code_file.read()

# create a module object
mod = types.ModuleType(module_name)
mod.__file__ = module_abs_file_path

# set a ref in sys.modules
sys.modules[module_name] = mod

# compile source code
code_obj = compile(source_code, filename=module_abs_file_path, mode='exec')

# execute compiled source code
exec(code_obj, mod.__dict__)

# now we can the function inside module1
mod.hello()

# it can imported too
import module1
module1.hello()