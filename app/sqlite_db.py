import sqlite3, os

DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))+'/db/'

db = sqlite3.connect(DATABASE_DIR+'python_subreddit.db')

def create_schema_db():
    with open(DATABASE_DIR+'schema.sql', mode='r') as schema_script:
        db.cursor().executescript(schema_script.read())
    db.commit()

def save_submissions(submissions):
    insert_submissions = """
    INSERT OR IGNORE INTO submissions
        (id, subreddit, title, submitter, discussion_url, url, punctuation, num_comments, created_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    db.cursor().executemany(insert_submissions, submissions)
    db.commit()

def get_tags(username):
    query = "SELECT id FROM tags WHERE username = ?"
    return db.cursor().execute(query, (username,)).fetchall()

def put_tag(username, tag):
    query = "SELECT MAX(id) FROM tags"
    max_ids = db.cursor().execute(query).fetchall()
    if max_ids[0][0] is None:
        max_id = 0
    else:
        max_id = 1 + max_ids[0][0]

    query = "INSERT INTO tags (username, tag, id) VALUES (?, ?, ?)"
    db.cursor().execute(query, (username, tag, max_id))
    db.commit()
    return max_id

def put_submission_tag(submission_id, tag_id):
    query = "INSERT INTO submissions_tags (submission_id, tag_id) VALUES (?, ?)"
    db.cursor().execute(query, (submission_id, tag_id))
    db.commit()

def get_submission_by_id(id):
    query = "SELECT * FROM submissions WHERE id = ?"
    return db.cursor().execute(query, (id,)).fetchall()

def get_submissions_by_submitter(submitter):
    query = "SELECT * FROM submissions WHERE submitter = ?"
    return db.cursor().execute(query, (submitter,)).fetchall()

def get_submissions_commented_by_user(user):
    query = """
    SELECT * FROM submissions WHERE id IN
        (SELECT submission_id FROM comments WHERE user = ?)
    """
    return db.cursor().execute(query, (user,)).fetchall()

def get_submissions(type, order_by):
    query = """
    SELECT s.id, s.title, s.subreddit, s.url,GROUP_CONCAT(at.all_tags)
    FROM submissions s
    LEFT JOIN submissions_tags st ON (st.submission_id = s.id)
    LEFT JOIN (SELECT t.id, t.tag all_tags FROM tags t) at ON (st.tag_id = at.id) GROUP BY s.id
    """

    if type == "external":
        query += " WHERE url NOT LIKE 'https://www.reddit.com%'"
    elif type == "internal":
        query += " WHERE url LIKE 'https://www.reddit.com%'"

    query += " ORDER BY " + order_by + " DESC LIMIT 10;"

    return db.cursor().execute(query).fetchall()

def save_submissions_comments(comments):
    insert_comments = """
    INSERT OR IGNORE INTO comments (id, parent_id, submission_id, user, text, punctuation)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    db.cursor().executemany(insert_comments, comments)
    db.commit()

# setting default to top 10
def get_top_submitters(limit=10):
    query = "SELECT submitter FROM submissions GROUP BY submitter ORDER BY count(*) DESC LIMIT ?"
    return db.cursor().execute(query, (limit,)).fetchall()

# setting default to top 10
def get_top_commenters(limit=10):
    return db.cursor().execute("SELECT user FROM comments GROUP BY user ORDER BY COUNT(*) DESC LIMIT ?", (limit,)).fetchall()

def save_users(users):
    insert_users = "INSERT OR IGNORE INTO users (username, comment_karma, post_karma) values (?, ?, ?)"
    db.cursor().executemany(insert_users, users)
    db.commit()

def get_user_comment_karma(username):
    return db.cursor().execute("SELECT comment_karma FROM users WHERE username=?", (username,)).fetchall()

def get_most_valued_users():
    return db.cursor().execute("SELECT * FROM users ORDER BY comment_karma+post_karma DESC LIMIT 10").fetchall()
