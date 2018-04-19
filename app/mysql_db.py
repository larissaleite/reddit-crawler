import MySQLdb, getpass
from defaults import DATABASE_DIR, DEFAULT_HOST, DEFAULT_USER, DEF_LIMIT

class MySQLDatabase(object):
    """Generic class for creating and writing to MySQL databases

    Parameters
    ----------
    db_name : str
        Corpus Database Name.
    table : str
        String which is added to beginning of MySQL table name.
    host : str
        Host that the MySQL server runs on.
    user : str
        Username for MySQL user.

    Returns
    -------
    MySQLDatabase object
    """
    
    def __init__(self, db_name, table, host=DEFAULT_HOST, user=DEFAULT_USER):
        self.db_name = db_name
        self.table = table
        self.host = host
        self.user = user
        self.connection = self.get_db_connection(db_name, host, user)

    def get_db_connection(self, db_name, host, user):
        return MySQLdb.connect (
                    host = host,
                    user = user,
                    db = db_name,
                    charset = 'utf8mb4',
                    use_unicode = True, 
                    read_default_file = "~/.my.cnf"
                )

    def create_schema_db(self):
        with open(DATABASE_DIR+'schema.sql', mode='r') as schema_script:
            query = " ".join(schema_script.readlines())
        for command in query.split(";"):
            c = " ".join(command.split())
            c = c.replace("NOT EXISTS ", "NOT EXISTS %s_" % self.table).replace("ALTER TABLE ", "ALTER TABLE %s_" % self.table)
            if c:
                print(c)
                self.connection.cursor().execute(c)

    def save_submissions(self, submissions):
        insert_submissions = """insert ignore into %s_submissions""" % self.table
        insert_submissions += """(id, title, text, submitter, discussion_url, url, punctuation, num_comments, created_date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.connection.cursor().executemany(insert_submissions, submissions)
        self.connection.commit()

    def get_submission_by_id(self, id):
        return self.connection.cursor().execute("select * from %s_submissions where id = %s;", (self.table, id,)).fetchall()

    def get_submissions_by_submitter(self, submitter):
        return self.connection.cursor().execute("select * from %s_submissions where submitter = %s;", (self.table, submitter,)).fetchall()

    def get_submissions_commented_by_user(self, user):
        return self.connection.cursor().execute("select * from %s_submissions where id in (select submission_id from comments where user = %s);", (self.table, user,)).fetchall()

    def get_submissions(self, type, order_by):
        query = "select * from %s_submissions" % self.table

        if type == "external":
            query += " where url NOT LIKE 'https://www.reddit.com%'"
        elif type == "internal":
            query += " where url LIKE 'https://www.reddit.com%'"

        query += " order by " + order_by + " desc limit 10;"

        return self.connection.cursor().execute(query).fetchall()

    def save_submissions_comments(self, comments):
        insert_comments = """insert ignore into %s_comments""" % self.table
        insert_comments += """(id, parent_id, submission_id, user, text, punctuation) values(%s, %s, %s, %s, %s, %s)"""
        self.connection.cursor().executemany(insert_comments, comments)
        self.connection.commit()

    def get_top_submitters(self, limit=DEF_LIMIT):
        return self.connection.cursor().execute("select submitter from submissions group by %s_submitter order by count(*) desc limit %s;" % (self.table, limit)).fetchall()

    def get_top_commenters(self, limit=DEF_LIMIT):
        return self.connection.cursor().execute("select user from %s_comments group by user order by count(*) desc limit %s;" % (self.table, limit)).fetchall()

    def save_users(self, users):
        insert_users = """insert ignore into %s_users""" % self.table
        insert_users += """(username, comment_karma, post_karma) values(%s, %s, %s)"""
        self.connection.cursor().executemany(insert_users, users)
        self.connection.commit()

    def get_user_comment_karma(self, username):
        return self.connection.cursor().execute("select comment_karma from %s_users where username=%s" % (self.table, username)).fetchall()

    def get_most_valued_users(self):
        return self.connection.cursor().execute("select * from %s_users order by comment_karma+post_karma desc limit %s;" % (self.table, limit)).fetchall()

