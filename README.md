# reddit-crawler

1. Run `pip install -r requirements.txt`
2. Run `python app/reddit_crawler.py <num_pages>` passing the number of pages to be crawled from Python subreddit
3. Run `python app/rest_api.py`
4. API calls on `localhost:5000/submissions?order_by=<num_comments/punctuation>&type=<external/internal>`
