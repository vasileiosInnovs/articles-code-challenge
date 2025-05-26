from db.connection import get_connection

class Magazine:

    all = {}

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all.update()

    def __repr__(self):
        return f'<Magazine {self.name}: Category {self.category}>'