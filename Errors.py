class InvalidObject(Exception):
    def __init__(self, obj):
        self.__init__("Invalid object")

class MissingKey(Exception):
    def __init__(self, key):
        self.__init__(f"Missing key: {key}")

class UnexpectedKey(Exception):
    def __init__(self, key):
        self.__init__(f"Unexpected key: {key}")

class UnknownDevice(Exception):
    def __init__(self):
        self.__init__("Unknown device")
