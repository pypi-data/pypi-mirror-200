class Granulometry:
    def __init__(self):
        
        self._name = "new granulometry"
        
        self._values = {}
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name