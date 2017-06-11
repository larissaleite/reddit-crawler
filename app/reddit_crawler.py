import requests, sys
import sqlite_db as db

def get_subreddit_data(subreddit, pages):
    all_submissions = []

    for page in range(0, pages):
        next_page = str()
        if page > 0:
            next_page = "after="+data['after']

        response = requests.get('https://www.reddit.com/r/'+subreddit+'/.json?'+next_page, headers = {'User-agent': 'lari_py_test'})
        data = response.json()['data']

        submissions = data['children']

        for submission in submissions:
            submission = submission['data']

            title = submission['title']
            submitter = submission['author']
            discussion_url = submission['permalink']
            url = submission['url']
            punctuation = submission['score']
            num_comments = submission['num_comments']
            created_date = submission['created']

            submission = (title, submitter, discussion_url, url, punctuation, num_comments, created_date)

            all_submissions.append(submission)

    save_submissions(all_submissions)

def save_submissions(submissions):
    db.save_submissions(submissions)

if __name__ == '__main__':
    db.init_db()
    get_subreddit_data('Python', int(sys.argv[1]))
