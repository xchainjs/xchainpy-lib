class AminoWrapping:
    def __init__(self, type : str , value):
        self._type = type
        self._value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value