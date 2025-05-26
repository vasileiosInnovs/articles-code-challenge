class Author:

    def __init__(self, name):
        self.name = name
        self.article = []

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str) or not (1 <= len(name) <= 25):
            raise ValueError("The name of the author has to be a string with a length of between 1 and 25")
        self._name = name