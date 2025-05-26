class Article:
    all = {}

    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.id}: {self.title} Author: {self.author_id} Magazine: {self.magazine_id}>'
    
    