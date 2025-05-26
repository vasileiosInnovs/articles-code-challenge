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
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
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
       cursor.execute(sql, (self.title, self.author_id, self.magazine_id))
       conn.commit()
       self.id = cursor.lastrowid
       
    @classmethod
    def create(cls, name):
        author = cls(name)
        author.save()
        return author

    @classmethod
    def instance_from_db(cls, row):
        article = cls.all.get(row[0])
        if article:
            article.title = row[1]
            article.author_id = row[2]
            article.magazine_id = row[3]
        else:
            article = cls(row[1], row[2], row[3])
            article.id = row[0]
            cls.all[article.id] = article
        return article
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM articles
            WHERE id = ?
        """

        row = cursor.execute(sql, (id, )).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM articles
            WHERE title = ?
        """
        row = cursor.execute(sql, (title,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM articles
            WHERE author_id = ?
        """

        row = cursor.execute(sql, (author_id, )).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM articles
            WHERE magazine_id = ?
        """

        row = cursor.execute(sql, (magazine_id, )).fetchone()
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
 