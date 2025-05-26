from db.connection import get_connection

class Magazine:

    all = {}

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all.update()

    def __repr__(self):
        return f'<Magazine {self.name}: Category {self.category}>'
    
    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name of magazine has to be a string")
        self._name = name