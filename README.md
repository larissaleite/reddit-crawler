[![Build Status](https://travis-ci.org/larissaleite/reddit-crawler.png)](https://travis-ci.org/larissaleite/reddit-crawler)

# reddit-crawler

1. Run `pip install -r requirements.txt`
2. To collect data from reddit run `python app/reddit_crawler.py <num_pages>` passing the number of pages to be crawled from Python subreddit
3. To start the API run `python app/rest_api.py`
4. API calls on `localhost:5000`:
    * `/api/submissions?order_by=num_comments,punctuation>&type=external,internal`
    * `/api/users/{username}/submissions`
    * `/api/users/{username}/comments/parent_submission`
    * `/api/users?order_by=num_comments/num_submissions/value`

### Assumptions:

* I tried to make it as generic/modular as possible, avoiding code repetition but keeping it simple enough to ease comprehension. For example, changing the database does not impact in the code for the crawler or the API.

* For efficiency purposes and to avoid overhead, I collected all the submissions, comments and user's info and sent to the database at once instead of inserting record by record.

* Within each request to the reddit_crawler to collect data from the last <num_pages> of the Python subreddit (although the code is easily adaptable to other subreddits), any new submission or comment is incorporated to the database. The ones who are already stored are not modified nor duplicated (using `insert or ignore`).
* It does not guarantee every new submission/comment will be gathered, but from what I understood the posts in the pages are not exactly ordered by date. My initial attempt was to update the archive by collecting all the submissions made after the date of the most recent post inserted on the database, but it was tricky and it seemed out of scope since the focus was to gather by pages instead of by date. So I decided to follow another approach that despite being simpler aims to cover all requirements.

* For the nested comments I don't think a relational database is the most suitable (although MySQL's nested set might suffice) as the structure favors very much the use of a document database such as MongoDB. However, since none of the queries exploited the nested structure of the comments, keeping it in SQLite was simpler.  

* Regarding user comment karma for a user, 10 most valued (best karma submissions+comments) users, I assumed from the requirements that this information would be required for every user who had submitted/commented on any of the retrieved submissions. So, I opted to store all the usernames in a global set and fill it as I crawled all the submissions/comments. After all submissions/comments are gathered, I collect the submission and comment karma for each user. This slows down the crawling a lot because a different request needs to be made to reddit for each user. In order to assess the performance of only crawling and storing data for submissions and comments, just comment the lines 21 and 22 of `app/reddit_crawler.py`. Another option could have been: after storing submissions and comments in the database, get all the users who are not yet in the table users and only for those get their information from reddit.
Additionally, the method `get_user_info(username)` works regardless of the data crawled from Python's subreddit, so it can be used to return the karma value for submissions and comments given any username.

* In addition to writing the queries from reddit's crawler and storing into SQLite, I added API calls to retrieve top submitters, top commenters, and 10 most valued (best karma submissions+comments) users; to query all posts by a user, all posts a user commented. The API calls only access data from the database, but the modifications would be minimal to allow it to be able to get data directly from reddit using `app/reddit_crawler.py`

* I included some extra functions that gathers submissions and comments given a username due to the assumption I had initially made from the requirements.
