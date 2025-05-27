import json
from pathlib import Path
from typing import Dict, Any, List


class Plugin:

    def __init__(self, plugin_path: str):
        self.plugin_path = Path(plugin_path)
        self.config = self._load_config()
        self.compendium_data = {}

    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración del plugin desde plugin.json"""
        config_path = self.plugin_path / "plugin.json"
        if not config_path.exists():
            raise FileNotFoundError(f"No se encontró plugin.json en {self.plugin_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @property
    def id(self) -> str:
        return self.config.get('id', self.plugin_path.name)

    @property
    def name(self) -> str:
        return self.config.get('name', self.id)

    @property
    def version(self) -> str:
        return self.config.get('version', '1.0.0')

    @property
    def description(self) -> str:
        return self.config.get('description', '')

    @property
    def author(self) -> str:
        return self.config.get('author', 'Unknown')

    @property
    def dependencies(self) -> List[str]:
        return self.config.get('dependencies', [])

    @property
    def priority(self) -> int:
        return self.config.get('priority', 0)

    @property
    def enabled(self) -> bool:
        return self.config.get('enabled', True)

    def load_compendium(self) -> Dict[str, Any]:
        """Carga el compendio del plugin en memoria"""
        if self.compendium_data:
            return self.compendium_data

        compendium_config = self.config.get('compendium', {})

        for data_type, file in compendium_config.items():
            full_path = self.plugin_path / 'compendium' / file
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        self.compendium_data[data_type] = json.load(f)
                        print(f"Cargado {data_type} desde {full_path}")
                except json.JSONDecodeError as e:
                    print(f"Error al cargar {file} en plugin {self.id}: {e}")
                    self.compendium_data[data_type] = {}
            else:
                print(f"Archivo no encontrado: {full_path}")
                self.compendium_data[data_type] = {}

        return self.compendium_data

    def get_data(self, data_type: str) -> Dict[str, Any]:
        """Obtiene datos específicos del compendio"""
        if not self.compendium_data:
            self.load_compendium()
        return self.compendium_data.get(data_type, {})

    def validate(self) -> bool:
        """Valida que el plugin esté correctamente configurado"""
        required_fields = ['id', 'name', 'version']
        return all(field in self.config for field in required_fields)
