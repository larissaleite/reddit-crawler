import requests, sys
import sqlite_db as db

BASE_URL = 'https://www.reddit.com/'

usernames = set()

def request_reddit_data(url):
    response = requests.get(BASE_URL+url, headers = {'User-agent': 'lari_py_test'})
    data = response.json()
    return data

def get_subreddit_pages(subreddit, pages):
    all_submissions = []
    all_submissions_comments = []

    next_page = str()
    for page in range(pages):
        print("Page %s of %s " % (page+1, pages))
        next_page = get_submissions_subreddit(subreddit,
                                              next_page,
                                              all_submissions,
                                              all_submissions_comments)

    print("Getting users info...")
    all_users_info = get_all_users_info()
    db.save_users(all_users_info)

    db.save_submissions(all_submissions)
    db.save_submissions_comments(all_submissions_comments)

def get_submissions_subreddit(subreddit, next_page, all_submissions, all_submissions_comments):
    url_params = "r/"+subreddit+"/.json?"+next_page
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

        submission = (submission_id, subreddit, title, submitter, discussion_url,
                      url, punctuation, num_comments, created_date)

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
        if 'author' not in comment:
            continue

        comment_id = comment['id']
        parent_id = comment['parent_id']
        user = comment['author']
        text = comment['body']
        punctuation = comment['score']

        all_comments.append((comment_id, parent_id, submission_id, user, text, punctuation))

        usernames.add(user)

        # recursively gets nested replies
        if comment['replies'] != "":
            replies = comment['replies']['data']['children']
            get_comments_data(replies, all_comments, submission_id)

def get_all_users_info():
    users = []
    for username in usernames:
        user = get_user_info(username)
        if isinstance(user, tuple): users.append(user)
    return users

def get_user_info(username):
    url_params = "user/"+username+"/about.json"

    user_info = request_reddit_data(url_params)

    try:
        user_info = user_info['data']

        comment_karma = user_info['comment_karma']
        post_karma = user_info['link_karma']

        user = (username, comment_karma, post_karma)
        return user
    except KeyError: # catches errors for example when user was deleted
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
    db.create_schema_db()

    try:
        subreddit = sys.argv[1]
        pages = int(sys.argv[2])

        if pages < 0: raise ValueError

        get_subreddit_pages(subreddit, pages)
    except (IndexError, ValueError):
        print "A valid number of pages needs to be passed as parameter"
