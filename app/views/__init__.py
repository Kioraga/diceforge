import os
from importlib import import_module

blueprints = []
for module in os.listdir(os.path.dirname(__file__)):
    if module.endswith('.py') and module not in ('__init__.py', '__pycache__'):
        module_name = module[:-3]  # Elimina '.py'
        mod = import_module(f'.{module_name}', package='views')
        if hasattr(mod, f'{module_name}_bp'):
            blueprints.append(getattr(mod, f'{module_name}_bp'))