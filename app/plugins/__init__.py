from .manager import PluginManager
from .plugin import Plugin
from .compendium import Compendium

# Instancias globales de PluginManager y Compendium
plugin_manager = PluginManager()
compendium = Compendium(plugin_manager)

__all__ = ['Plugin', 'plugin_manager', 'compendium']
