```markdown
# 📰 Articles Code Challenge

A Python project that models a many-to-many relationship between Authors, Magazines, and Articles using SQLite and Object-Oriented Programming (OOP). Each Author can write many Articles, and each Article belongs to one Magazine.

---

## 📁 Project Structure

```

articles-code-challenge/
├── lib/                      # Main code directory
│   ├── models/       
│   │   ├── __init__.py       # Makes models a package
│   │   ├── author.py         # Author model with SQL + logic
│   │   ├── article.py        # Article model with SQL + logic
│   │   └── magazine.py       # Magazine model with SQL + logic
│   ├── db/
│   │   ├── __init__.py       # Makes models a package
│   │   ├── connection.py     # SQLite database connection
│   │   ├── seed.py           # Seed data to populate the database
│   │   └── schema.sql        # Optional: schema-only setup
│   ├── controllers/
|   |   └── __init__.py 
│   ├── debug.py              # Interactive ipdb session
│   └── **init**.py
├── scripts/
│   └── setup\_db.py           # Setup utility 
├── tests/
│   └── test\_\*.py             # Unit tests (TBD)
└── README.md                 # Project documentation

````

---

## ⚙️ Requirements

- Python 3.8+
- SQLite3
- [`ipdb`](https://pypi.org/project/ipdb/) for debugging (optional but useful)

Install dependencies with:

```bash
pip install ipdb
````

---

## 🚀 Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/vasileiosInnovs/articles-code-challenge
cd articles-code-challenge
```

2. **Run the seed script** to create tables and insert sample data:

```bash
python3 -m lib.db.seed
```

3. **Explore interactively** using `ipdb`:

```python
ipdb> Author.find_by_name("Alice Walker")
ipdb> tech = Magazine.find_by_name("Tech Monthly")
ipdb> tech
```

---

## 🧠 Features

* `Author.create(name)` — Create an author and save to DB
* `Magazine.create(name, category)` — Create a magazine
* `Article(title, author_id, magazine_id).save()` — Add an article
* `Author#articles()` — Get all articles by author
* `Author#magazines()` — Get magazines written for
* `Magazine#articles()` — Get all articles in magazine
* `Article.find_by_title(title)` — Lookup article

---

## 🧪 Testing

Test files can go under the `tests/` directory and use `unittest` or `pytest`. You can run them like:

```bash
python3 -m unittest discover tests
```

---

## ❓ Troubleshooting

**Q:** I get `ModuleNotFoundError: No module named 'lib'`
**A:** Always run Python modules using `-m` from the root:

```bash
python3 -m lib.db.seed
```

---

## 📚 Learn More

* [SQLite Documentation](https://www.sqlite.org/docs.html)
* [Python `sqlite3` module](https://docs.python.org/3/library/sqlite3.html)
* [Python OOP Basics](https://realpython.com/python3-object-oriented-programming/)

---

## 📄 License

MIT License. Free to use, learn from, and modify.

```

---

Let me know if you want this as a downloadable file or want help customizing it for deployment, publishing, or contributing guidelines.
```
