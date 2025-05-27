from .manager import PluginManager
from .plugin import Plugin

# Instancia global del gestor de plugins
plugin_manager = PluginManager()

__all__ = ['PluginManager', 'Plugin', 'plugin_manager']