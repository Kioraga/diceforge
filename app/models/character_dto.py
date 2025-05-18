import sirope


class CharacterDto:
    def __init__(self, name, char_class, level):
        self._id = None
        self._name = name
        self._class = char_class
        self._level = level

    @property
    def name(self):
        return self._name

    @property
    def char_class(self):
        return self._class

    @property
    def level(self):
        return self._level

    def get_id(self):
        return self._id

    @staticmethod
    def find(s: sirope.Sirope, character_id: str) -> "CharacterDto":
        return s.find_first(CharacterDto, lambda c: c.get_id() == character_id)
