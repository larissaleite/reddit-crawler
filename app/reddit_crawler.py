import requests, sys, argparse
from mysql_db import MySQLDatabase
from defaults import BASE_URL, DEFAULT_DB, DEFAULT_HOST, DEFAULT_USER, DEFAULT_SUB_REDDIT, DEFAULT_PAGES, DEFAULT_TABLE_PREFIX

usernames = set()

def request_reddit_data(url):
    response = requests.get(BASE_URL+url, headers = {'User-agent': 'lari_py_test'})
    data = response.json()
    return data

def get_subreddit_pages(subreddit, pages):
    all_submissions = []
    all_submissions_comments = []

    next_page = str()
    for page in range(0, pages):
        next_page = get_submissions_subreddit("r/"+subreddit+"/.json?"+next_page, all_submissions, all_submissions_comments)

    all_users_info = get_all_users_info()
    db.save_users(all_users_info)

    db.save_submissions(all_submissions)
    db.save_submissions_comments(all_submissions_comments)

def get_submissions_subreddit(url_params, all_submissions, all_submissions_comments):
    data = request_reddit_data(url_params)['data']

    submissions = data['children']

    for submission in submissions:
        submission = submission['data']

        submission_id = submission['id']
        title = submission['title']
        submitter = submission['author']
        discussion_url = submission['permalink']
        url = submission['url']
        punctuation = submission['score']
        num_comments = submission['num_comments']
        created_date = submission['created']
        text = submission['selftext']

        submission = (submission_id, title, text, submitter, discussion_url, url, punctuation, num_comments, created_date)

        all_submissions.append(submission)

        all_submissions_comments += get_submission_comments(submission_id, discussion_url)

        usernames.add(submitter)

    next_page = "after="+data['after']
    return next_page

def get_submission_comments(submission_id, comments_url):
    all_comments = []

    url_params = comments_url+".json"
    data = request_reddit_data(url_params)

    #ignores the submission itself
    data = data[1]
    comments = data['data']['children']

    get_comments_data(comments, all_comments, submission_id)

    return all_comments

def get_comments_data(comments, all_comments, submission_id):
    for comment in comments:
        comment = comment['data']

        comment_id = comment['id']
        parent_id = comment['parent_id']
        user = comment['author'] if 'author' in comment else ''
        text = comment['body'] if 'body' in comment else ''
        punctuation = comment['score'] if 'score' in comment else ''

        all_comments.append((comment_id, parent_id, submission_id, user, text, punctuation))

        usernames.add(user)

        # recursively gets nested replies
        if 'replies' in comment and comment['replies'] != "":
            replies = comment['replies']['data']['children']
            get_comments_data(replies, all_comments, submission_id)

def get_all_users_info():
    users = []
    for username in usernames:
        user = get_user_info(username)
        if isinstance(user, tuple): users.append(user)
    return users

def get_user_info(username):
    try:
        url_params = "user/"+username+"/about.json"
        user_info = request_reddit_data(url_params)

        user_info = user_info['data']

        comment_karma = user_info['comment_karma']
        post_karma = user_info['link_karma']

        user = (username, comment_karma, post_karma)
        return user
    except (TypeError, KeyError): # catches errors for example when user was deleted
        return "Invalid username"

def get_user_posts(username):
    all_user_submissions = []

    next_page = str()

    while next_page != "null":
        url_params = "user/"+username+"/submitted/.json?after="+next_page
        data = request_reddit_data(url_params)['data']

        user_submissions = data['children']
        all_submissions.append(user_submissions)

    return all_user_submissions

def get_posts_user_commented(username):
    all_user_comments = []

    next_page = str()

    while next_page != "null":
        url_params = "user/"+username+"/comments/.json?after="+next_page
        data = request_reddit_data(url_params)['data']

        user_comments = data['children']
        all_user_comments.append(user_comments)

    return all_user_comments

if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser(description='Collect data from Reddit and store in MySQL')
    
    parser.add_argument('-d', '--database', dest='db_name', default=DEFAULT_DB, 
        help='MySQL database where tweets will be stored. Default: %s' % (DEFAULT_DB))
    parser.add_argument('-t', '--table_prefix', dest='table_prefix', default=DEFAULT_TABLE_PREFIX, 
        help='String to be added to beginning of MySQL table names. Default: %s' % (DEFAULT_TABLE_PREFIX))
    parser.add_argument('-H', '--host', dest='host', default=DEFAULT_HOST, 
        help='MySQL host. Default: %s' % (DEFAULT_HOST))
    parser.add_argument('-u', '--user', dest='user', default=DEFAULT_USER, 
        help='MySQL username. Default: %s' % (DEFAULT_USER))
    parser.add_argument('-s', '--subreddit', dest='subreddit', default=DEFAULT_SUB_REDDIT, 
        help='Name of subreddit to search. Default: %s' % (DEFAULT_SUB_REDDIT))
    parser.add_argument('-p', '--pages', dest='pages', default=DEFAULT_PAGES, type=int,
        help='Number of pages to search. Default: %s' % (DEFAULT_PAGES))

    args = parser.parse_args()

    if not args.db_name:
        print("Must supply a databse name via -d or --database.")
        sys.exit(1)

    if int(args.pages) < 0:
        print("Page number most be non-negative.")
        sys.exit(1)

    if not args.table_prefix:
        print("Table prefix set to %s" % args.subreddit.lower())
        args.table_prefix = args.subreddit.lower()

    db = MySQLDatabase(db_name=args.db_name, table=args.table_prefix, host=args.host, user=args.user)
    db.create_schema_db()

    get_subreddit_pages(args.subreddit, int(args.pages))
    
