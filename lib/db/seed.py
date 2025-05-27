#!/usr/bin/env python3

from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Drop tables if they exist
Author.drop_table()
Magazine.drop_table()
Article.drop_table()

# Recreate tables
Author.create_table()
Magazine.create_table()
Article.create_table()

# Create Authors
alice = Author.create("Alice Walker")
bob = Author.create("Bob Dylan")
clara = Author.create("Clara Hughes")

# Create Magazines
tech = Magazine("Tech Monthly", "Technology")
travel = Magazine("Wanderlust", "Travel")
music = Magazine("Sound Sphere", "Music")

tech.save()
travel.save()
music.save()

# Create Articles
article1 = Article("The Rise of AI", alice.id, tech.id)
article1.save()

article2 = Article("Top 10 Travel Destinations", bob.id, travel.id)
article2.save()

article3 = Article("The Soul of Music", clara.id, music.id)
article3.save()

article4 = Article("AI in Travel", alice.id, travel.id)
article4.save()

article5 = Article("Folk Revival", bob.id, music.id)
article5.save()


import ipdb
ipdb.set_trace()
