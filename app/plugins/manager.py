import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from .plugin import Plugin


class PluginManager:
    """Gestor principal de plugins"""

    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins: Dict[str, Plugin] = {}
        self.loaded = False

    def _discover_plugins(self) -> List[str]:
        """Descubre todos los plugins disponibles"""
        if not self.plugins_dir.exists():
            os.makedirs(self.plugins_dir, exist_ok=True)
            return []

        plugin_dirs = []
        for item in self.plugins_dir.iterdir():
            if item.is_dir() and (item / "plugin.json").exists():
                plugin_dirs.append(item.name)

        return plugin_dirs

    def load_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """Carga un plugin específico"""
        plugin_path = self.plugins_dir / plugin_id

        if not plugin_path.exists():
            print(f"Plugin {plugin_id} no encontrado")
            return None

        try:
            plugin = Plugin(str(plugin_path))
            if not plugin.validate():
                print(f"Plugin {plugin_id} no es válido")
                return None

            if plugin.enabled:
                plugin.load_compendium()
                self.plugins[plugin_id] = plugin
                print(f"Plugin {plugin.name} v{plugin.version} cargado exitosamente")
                return plugin
            else:
                print(f"Plugin {plugin_id} está deshabilitado")

        except Exception as e:
            print(f"Error al cargar plugin {plugin_id}: {e}")

        return None

    def load_all_plugins(self):
        """Carga todos los plugins disponibles"""
        plugin_dirs = self._discover_plugins()

        # Cargar plugins ordenados por prioridad
        plugins_to_load = []
        for plugin_dir in plugin_dirs:
            try:
                temp_plugin = Plugin(str(self.plugins_dir / plugin_dir))
                if temp_plugin.enabled:
                    plugins_to_load.append((temp_plugin.priority, plugin_dir, temp_plugin))
            except Exception as e:
                print(f"Error al evaluar plugin {plugin_dir}: {e}")

        # Ordenar por prioridad (mayor prioridad primero)
        plugins_to_load.sort(key=lambda x: x[0], reverse=True)

        # Cargar plugins en orden de prioridad
        for priority, plugin_dir, temp_plugin in plugins_to_load:
            if self._check_dependencies(temp_plugin.dependencies):
                self.load_plugin(plugin_dir)
            else:
                print(f"Plugin {plugin_dir} tiene dependencias no satisfechas: {temp_plugin.dependencies}")

        self.loaded = True
        print(f"Se cargaron {len(self.plugins)} plugins")

    def _check_dependencies(self, dependencies: List[str]) -> bool:
        """Verifica que las dependencias estén satisfechas"""
        for dep in dependencies:
            if dep not in self.plugins:
                return False
        return True

    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """Obtiene un plugin por su ID"""
        return self.plugins.get(plugin_id)

    def get_all_data(self, data_type: str) -> Dict[str, Any]:
        """Obtiene todos los datos de un tipo específico de todos los plugins"""
        if not self.loaded:
            self.load_all_plugins()

        combined_data = {}
        for plugin in self.plugins.values():
            plugin_data = plugin.get_data(data_type)
            combined_data.update(plugin_data)

        return combined_data

    def reload_plugins(self):
        """Recarga todos los plugins"""
        self.plugins.clear()
        self.loaded = False
        self.load_all_plugins()

    def enable_plugin(self, plugin_id: str):
        """Habilita un plugin"""
        plugin_path = self.plugins_dir / plugin_id / "plugin.json"
        if plugin_path.exists():
            with open(plugin_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            config['enabled'] = True

            with open(plugin_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"Plugin {plugin_id} habilitado")

            self.load_plugin(plugin_id)

    def disable_plugin(self, plugin_id: str):
        """Deshabilita un plugin"""
        if plugin_id in self.plugins:
            del self.plugins[plugin_id]

        plugin_path = self.plugins_dir / plugin_id / "plugin.json"
        if plugin_path.exists():
            with open(plugin_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            config['enabled'] = False

            with open(plugin_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"Plugin {plugin_id} deshabilitado")

    def list_plugins(self) -> List[Plugin]:
        """Lista todos los plugins con su información"""
        all_plugins = []

        for plugin_dir in self._discover_plugins():
            try:
                plugin_path = self.plugins_dir / plugin_dir
                temp_plugin = Plugin(str(plugin_path))
                all_plugins.append(temp_plugin)
            except Exception as e:
                print(f"Error al procesar plugin {plugin_dir}: {e}")

        return all_plugins

    def get_enabled_plugins(self) -> List[Plugin]:
        """Obtiene una lista de todos los plugins habilitados"""
        return [plugin for plugin in self.plugins.values() if plugin.enabled]
