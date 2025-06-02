from lib.db.connection import get_connection
from lib.models.author import Author
import sqlite3

class Magazine:

    all = {}

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

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
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def drop_table(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DROP TABLE IF EXISTS magazines;"
        cursor.execute(sql)
        conn.commit()

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?, ?)
        """
        cursor.execute(sql, (self.name, self.category))
        conn.commit()

        self.id = cursor.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine

    @classmethod
    def instance_from_db(cls, row):
        magazine = cls.all.get(row[0])
        if magazine:
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            magazine = cls(row[1], row[2], id=row[0])
            cls.all[magazine.id] = magazine
        return magazine
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM magazines WHERE id = ?"
        row = cursor.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM magazines WHERE category = ?"
        row = cursor.execute(sql, (category,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM magazines WHERE name = ?"
        row = cursor.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = """
            SELECT DISTINCT au.*
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
        """, (self.id,)
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT DISTINCT au.*
            FROM authors au
            JOIN articles a ON a.author_id = au.id
            WHERE a.magazine_id = ?
        """
        rows = cursor.execute(sql, (self.id,)).fetchall()

        return [Author.instance_from_db(row) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT title FROM articles
            WHERE magazine_id = ?
        """
        rows = cursor.execute(sql, (self.id,)).fetchall()

        return set([row[0] for row in rows])

    def contributing_authors(self):
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT a.author_id, au.name
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()

        authors = [row['name'] for row in rows]
        return authors 
    
    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT m.id, m.name, COUNT(DISTINCT a.author_id) AS author_count
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING author_count > 1
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        magazines = []

        for row in rows:
            magazine = cls(name=row[1], category=row[2])
            magazine.id = row[0]
            magazines.append(magazine)

        return magazines
    
    @classmethod
    def article_counts(cls):
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = """
            SELECT m.id, m.name, m.category, COUNT(a.id) as article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """

        rows = cursor.execute(sql).fetchall()
        return rows