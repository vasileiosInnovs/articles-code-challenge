#!/usr/bin/env python3

from db.connection import get_connection
from models.author import Author
#from models.article import Article

import ipdb

Author.create_table()
#Article.create_table()

ipdb.set_trace()