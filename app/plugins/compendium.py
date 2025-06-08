import re
from typing import Dict, Any, List, Optional
from .manager import PluginManager


class Compendium:
    """Clase para acceder a todos los datos del compendio de forma centralizada"""

    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager

    def _ensure_plugins_loaded(self):
        """Asegura que los plugins estén cargados"""
        if not self.plugin_manager.loaded:
            self.plugin_manager.load_all_plugins()

    def _get_all_data(self, data_type: str) -> Dict[str, Any]:
        """Método interno para obtener todos los datos de un tipo"""
        self._ensure_plugins_loaded()
        return self.plugin_manager.get_all_data(data_type)

    def _get_single_item(self, data_type: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Método interno para obtener un elemento específico"""
        all_items = self._get_all_data(data_type).get('entries', {})
        return all_items.get(item_id)

    def _search_items(self, data_type: str, **filters) -> Dict[str, Any]:
        """Método interno para filtrar elementos"""
        all_items = self._get_all_data(data_type).get('entries', {})
        filtered_items = {}

        for item_id, item_data in all_items.items():
            match = True
            for key, value in filters.items():
                if key not in item_data:
                    match = False
                    break
                if isinstance(value, list):
                    if item_data[key] not in value:
                        match = False
                        break
                elif item_data[key] != value:
                    match = False
                    break

            if match:
                filtered_items[item_id] = item_data

        return filtered_items

    # Métodos para razas
    def get_races(self) -> Dict[str, Any]:
        """Obtiene todas las razas disponibles"""
        return self._get_all_data('races').get('entries', {})

    def get_race(self, race_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una raza específica por ID"""
        return self._get_single_item('races', race_id)

    def race_names(self) -> List[Any]:
        """Obtiene los nombres de todas las razas disponibles"""
        return [race.get('name', '') for race in self.get_races().values()]

    def get_race_id(self, race_name: str) -> Optional[str]:
        """Obtiene el ID de una raza por su nombre"""
        for race_id, race_data in self.get_races().items():
            if race_data.get('name') == race_name:
                return race_id
        return None

    # Métodos para clases
    def get_classes(self) -> Dict[str, Any]:
        """Obtiene todas las clases disponibles"""
        return self._get_all_data('classes').get('entries', {})

    def get_class(self, class_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una clase específica por ID"""
        return self._get_single_item('classes', class_id)

    def class_names(self) -> List[Any]:
        """Obtiene los nombres de todas las clases disponibles"""
        return [cls.get('name', '') for cls in self.get_classes().values()]

    def get_class_id(self, class_name: str) -> Optional[str]:
        """Obtiene el ID de una clase por su nombre"""
        for cls_id, cls_data in self.get_classes().items():
            if cls_data.get('name') == class_name:
                return cls_id
        return None

    def get_class_hp(self, class_name: str) -> Optional[int]:
        """Obtiene los puntos de golpe base de una clase por su nombre"""
        description = self.get_class(class_name).get('description', {})

        match = re.search(r'1:</strong>\s*(\d+)', description)
        return int(match.group(1)) if match else None

    # Métodos para hechizos
    def get_spells(self) -> Dict[str, Any]:
        """Obtiene todos los hechizos disponibles"""
        return self._get_all_data('spells').get('entries', {})

    def get_spell(self, spell_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un hechizo específico por ID"""
        return self._get_single_item('spells', spell_id)

    def get_spells_by_level(self, level: int) -> Dict[str, Any]:
        """Obtiene hechizos filtrados por nivel"""
        return self._search_items('spells', level=level)

    def get_cantrips(self) -> Dict[str, Any]:
        """Obtiene todos los cantrips (hechizos de nivel 0)"""
        return self.get_spells_by_level(0)

    # Métodos para subclases
    def get_subclasses(self) -> Dict[str, Any]:
        """Obtiene todas las subclases disponibles"""
        return self._get_all_data('subclasses').get('entries', {})

    def get_subclass(self, subclass_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una subclase específica por ID"""
        return self._get_single_item('subclasses', subclass_id)

    def get_subclasses_for_class(self, class_name: str) -> Dict[str, Any]:
        """Obtiene subclases para una clase específica"""
        subclasses_names = self.get_class(class_name).get('subclasses', [])
        return {name: self.get_subclass(name) for name in subclasses_names if self.get_subclass(name)}

    # Métodos para trasfondos
    def get_backgrounds(self) -> Dict[str, Any]:
        """Obtiene todos los trasfondos disponibles"""
        return self._get_all_data('backgrounds').get('entries', {})

    def get_background(self, background_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un trasfondo específico por ID"""
        return self._get_single_item('backgrounds', background_id)

    # Otras utilidades
    def get_available_data_types(self) -> List[str]:
        """Obtiene todos los tipos de datos disponibles"""
        self._ensure_plugins_loaded()
        data_types = set()

        for plugin in self.plugin_manager.plugins.values():
            data_types.update(plugin.compendium_data.keys())

        return sorted(list(data_types))

    def get_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas del compendium"""
        stats = {}
        for data_type in self.get_available_data_types():
            stats[data_type] = len(self._get_all_data(data_type).get('entries', {}))

        return stats
