import sqlite3, os

DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))+'/db/'

# helper function to return JSON from SQLite queries
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_schema_db():
    db = get_db()
    with open(DATABASE_DIR+'schema.sql', mode='r') as schema_script:
        db.cursor().executescript(schema_script.read())
    db.commit()

def get_db():
    sqlite_connection = sqlite3.connect(DATABASE_DIR+'python_subreddit.db')
    sqlite_connection.row_factory = dict_factory
    return sqlite_connection

def save_submissions(submissions):
    db = get_db()

    insert_submissions = 'insert or ignore into submissions(id, title, submitter, discussion_url, url, punctuation, num_comments, created_date) values(?, ?, ?, ?, ?, ?, ?, ?)'
    db.cursor().executemany(insert_submissions, submissions)
    db.commit()

def get_submission_by_id(id):
    db = get_db()

    return db.cursor().execute("select * from submissions where id = '%s';" %id).fetchall()

def get_submissions_by_submitter(submitter):
    db = get_db()

    return db.cursor().execute("select * from submissions where submitter = '%s';" %submitter).fetchall()

def get_submissions_commented_by_user(user):
    db = get_db()

    return db.cursor().execute("select * from submissions where id in (select submission_id from comments where user = '%s');" %user).fetchall()

def get_submissions(type, order_by):
    query = "select * from submissions"

    if type == "external":
        query += " where url NOT LIKE 'https://www.reddit.com%'"
    elif type == "internal":
        query += " where url LIKE 'https://www.reddit.com%'"

    query += " order by " + order_by + " desc limit 10;"

    return get_db().cursor().execute(query).fetchall()

def save_submissions_comments(comments):
    db = get_db()

    insert_comments = 'insert or ignore into comments(id, parent_id, submission_id, user, text, punctuation) values(?, ?, ?, ?, ?, ?)'
    db.cursor().executemany(insert_comments, comments)
    db.commit()


# setting default to top 10
def get_top_submitters(limit=10):
    db = get_db()

    return db.cursor().execute("select submitter from submissions group by submitter order by count(*) desc limit "+str(limit)+";").fetchall()

# setting default to top 10
def get_top_commenters(limit=10):
    db = get_db()

    return db.cursor().execute("select user from comments group by user order by count(*) desc limit "+str(limit)+";").fetchall()

def save_users(users):
    db = get_db()

    insert_users = 'insert or ignore into users(username, comment_karma, post_karma) values(?, ?, ?)'
    db.cursor().executemany(insert_users, users)
    db.commit()

def get_user_comment_karma(username):
    db = get_db()

    return db.cursor().execute("select comment_karma from users where username='%s'" %username).fetchall()

def get_most_valued_users():
    db = get_db()

    return db.cursor().execute("select * from users order by comment_karma+post_karma desc limit 10;").fetchall()
