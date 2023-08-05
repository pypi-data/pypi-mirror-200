from .gasset import GAsset


def type_to_str(t):
    
    t = str(t)

    if "int" in t:
        return "int"
    elif "float" in t:
        return "float"
    elif "dict" in t:
        return "json"
    elif "bool" in t:
        return "boolean"
    else:
        return "invalid"

class Log(GAsset):
    def __init__(self, name, value, title=None, description=None, var=None, messageType="file"):
        super().__init__(name=name, title=title, description=description, var=var, messageType=messageType)
        self.set_value(value)

    def to_json(self):
        
        result = super().to_json()
        result['path'] = None
        result['value'] = self.value
        result['valueType'] = type_to_str(self.valueType)
        return result

    def set_value(self, newValue):
        self.value = newValue
        self.valueType = type(self.value)
