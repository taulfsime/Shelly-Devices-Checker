class InvalidObject(Exception):
    def __init__(self, obj):
        super().__init__("Invalid object")

class MissingKey(Exception):
    def __init__(self, key):
        super().__init__(f"Missing key: {key}")

class UnexpectedKey(Exception):
    def __init__(self, key):
        super().__init__(f"Unexpected key: {key}")

class UnknownDevice(Exception):
    def __init__(self, deviceIP):
        super().__init__(f"Unknown device ({deviceIP})")
