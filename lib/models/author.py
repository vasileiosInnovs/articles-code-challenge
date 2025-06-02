from lib.db.connection import get_connection 

class Author:

    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        self._article = []
        self._magazine = []

    def __repr__(self):
        return f'<Author {self.id}: {self.name}>'

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str) or not (1 <= len(name) <= 50):
            raise ValueError("The name of the author has to be a string with a length of between 1 and 25")
        self._name = name

    @classmethod
    def create_table(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
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

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO authors (name) VALUES (?)
        """

        cursor.execute(sql, (self.name,))
        conn.commit()

        self.id = cursor.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name):
        author = cls(name)
        author.save()
        return author
    
    @classmethod
    def instance_from_db(cls, row):
        author = cls.all.get(row[0])
        if author:
            author.name = row[1]
        else:
            author = cls(row[1])
            author.id = row[0]
            cls.all[author.id] = author
        return author

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM authors
            WHERE id = ?
        """

        row = cursor.execute(sql, (id, )).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM authors
            WHERE name = ?
        """
        row = cursor.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM authors
        """
        rows = cursor.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM articles
            WHERE author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        return rows
    
    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.*
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        return rows
    
    def add_article(self, magazine, title):
        from lib.models.article import Article

        article = Article(title, self.id, magazine.id)
        article.save()
        return article
    
    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT DISTINCT m.category
            FROM magazine m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """

        cursor.execute(sql , (self.id,))
        rows = cursor.fetchall()

        return [row[0] for row in rows]
    
    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
    
        sql = """
            SELECT a.id, a.name, COUNT(ar.id) AS article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """
    
        row = cursor.execute(sql).fetchone()
        if row:
            author = cls(name=row[1])
            author.id = row[0]
            return author
        else:
            return None