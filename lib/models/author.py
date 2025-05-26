from db.connection import get_connection

class Author:

    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        self._article = []

    def __repr__(self):
        return f'<Author {self.id}: {self.name}>'

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str) or not (1 <= len(name) <= 25):
            raise ValueError("The name of the author has to be a string with a length of between 1 and 25")
        self._name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO authors (name) VALUES (?)
        """

        cursor.execute(sql)
        conn.commit()

        self.id = cursor.lastrowid

    @classmethod
    def create(cls, name):
        author = cls(name)
        author.save()
        return author

    @classmethod
    def create_table(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT
            )
        """

        cursor.execute(sql)
        conn.commit()

    @classmethod
    def drop_table(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            DROP TABLE IF EXISTS authors;
        """
        cursor.execute(sql)
        conn.commit()

    