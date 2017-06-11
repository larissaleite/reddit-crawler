import sqlite3, os

DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))+'/db/'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    sqlite_connection = sqlite3.connect(DATABASE_DIR+'python_subreddit.db')
    sqlite_connection.row_factory = dict_factory
    return sqlite_connection

def init_db():
    db = get_db()
    with open(DATABASE_DIR+'schema.sql', mode='r') as schema_script:
        db.cursor().executescript(schema_script.read())
    db.commit()

def save_submissions(submissions):
    db = get_db()

    insert_submissions = 'insert into submission(title, submitter, discussion_url, url, punctuation, num_comments, created_date) values(?, ?, ?, ?, ?, ?, ?)'
    db.cursor().executemany(insert_submissions, submissions)
    db.commit()

def get_submissions(type, order_by):
    query = "select * from submission"

    if type == "external":
        query += " where url NOT LIKE 'https://www.reddit.com%'"
    elif type == "internal":
        query += " where url LIKE 'https://www.reddit.com%'"

    query += " order by " + order_by + " desc limit 10;"

    return get_db().cursor().execute(query).fetchall()
