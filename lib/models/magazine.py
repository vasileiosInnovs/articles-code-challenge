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

    @classmethod
    def create_table(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL
            )
        """
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def drop_table(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            DROP TABLE IF EXISTS magazines;
        """

        cursor.execute(sql)
        conn.commit()

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO magazines (self.name, self.category)
            VALUES (?, ?)
        """

        cursor.execute(sql, (self.name, self.category))
        conn.commit()

        self.id = cursor.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name):
        magazine = cls(name)
        magazine.save()
        return magazine
