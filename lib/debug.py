#!/usr/bin/env python3

from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

import ipdb  

# Create tables
Author.create_table()
Magazine.create_table()
Article.create_table()

# Optional: Drop tables first to reset the DB
# Author.drop_table()
# Magazine.drop_table()
# Article.drop_table()

# Create sample authors
a1 = Author.create("Alice")
a2 = Author.create("Bob")

# Create sample magazines
m1 = Magazine("Tech Monthly", "Technology")
m2 = Magazine("Health Weekly", "Health")
m1.save()
m2.save()

# Create sample articles
article1 = Article("AI Future", a1.id, m1.id)
article1.save()

article2 = Article("Wellness Tips", a2.id, m2.id)
article2.save()

article3 = Article("Tech in 2025", a1.id, m1.id)
article3.save()

# Interactive shell to explore
ipdb.set_trace()
