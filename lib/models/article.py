from db.connection import get_connection

class Article:
    all = {}

    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.id}: {self.title} Author: {self.author_id} Magazine: {self.magazine_id}>'
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if not isinstance(title, str) or not (1 <= len(title) <= 25):
            raise ValueError("The title of the article has to be a string")
        self._title = title

    @classmethod
    def create_table(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author_id INTEGER,
            magazine_id INTEGER
            )
        """

        cursor.execute(sql)
        conn.commit()

    @classmethod
    def drop_table(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            DROP TABLE IF EXISTS articles;
        """
        cursor.execute(sql)
        conn.commit()

    def save(self):
       conn = get_connection()
       cursor = conn.cursor()
       sql = """
           INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)
       """
       cursor.execute(sql)
       conn.commit()
       self.id = cursor.lastrowid