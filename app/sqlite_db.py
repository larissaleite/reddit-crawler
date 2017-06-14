import sqlite3, os

DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))+'/db/'

db = sqlite3.connect(DATABASE_DIR+'python_subreddit.db')

def create_schema_db():
    with open(DATABASE_DIR+'schema.sql', mode='r') as schema_script:
        db.cursor().executescript(schema_script.read())
    db.commit()

def save_submissions(submissions):
    insert_submissions = 'insert or ignore into submissions(id, title, submitter, discussion_url, url, punctuation, num_comments, created_date) values(?, ?, ?, ?, ?, ?, ?, ?)'
    db.cursor().executemany(insert_submissions, submissions)
    db.commit()

def get_submission_by_id(id):
    return db.cursor().execute("select * from submissions where id = ?;", (id,)).fetchall()

def get_submissions_by_submitter(submitter):
    return db.cursor().execute("select * from submissions where submitter = ?;", (submitter,)).fetchall()

def get_submissions_commented_by_user(user):
    return db.cursor().execute("select * from submissions where id in (select submission_id from comments where user = ?);", (user,)).fetchall()

def get_submissions(type, order_by):
    query = "select * from submissions"

    if type == "external":
        query += " where url NOT LIKE 'https://www.reddit.com%'"
    elif type == "internal":
        query += " where url LIKE 'https://www.reddit.com%'"

    query += " order by " + order_by + " desc limit 10;"

    return db.cursor().execute(query).fetchall()

def save_submissions_comments(comments):
    insert_comments = 'insert or ignore into comments(id, parent_id, submission_id, user, text, punctuation) values(?, ?, ?, ?, ?, ?)'
    db.cursor().executemany(insert_comments, comments)
    db.commit()

# setting default to top 10
def get_top_submitters(limit=10):
    return db.cursor().execute("select submitter from submissions group by submitter order by count(*) desc limit ?;", (limit,)).fetchall()

# setting default to top 10
def get_top_commenters(limit=10):
    return db.cursor().execute("select user from comments group by user order by count(*) desc limit ?;", (limit,)).fetchall()

def save_users(users):
    insert_users = 'insert or ignore into users(username, comment_karma, post_karma) values(?, ?, ?)'
    db.cursor().executemany(insert_users, users)
    db.commit()

def get_user_comment_karma(username):
    return db.cursor().execute("select comment_karma from users where username=?", (username,)).fetchall()

def get_most_valued_users():
    return db.cursor().execute("select * from users order by comment_karma+post_karma desc limit 10;").fetchall()
