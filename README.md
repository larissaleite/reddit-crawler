# reddit-crawler-mysql

Fork of [reddit-crawler](https://github.com/larissaleite/reddit-crawler):
- Works with MySQL database instead of SQLite
- `MySQLDatabase` class added
- Added argparse
- Separated defaults into a separate py file: `app/defaults.py`

## Installation

1. Run `pip install -r requirements.txt`
2. To collect data from reddit run `python app/reddit_crawler.py -d <database> -s <subreddit>`
3. To start the API run `python app/rest_api.py`
4. API calls on `localhost:5000`:
    * `/api/submissions?order_by=num_comments,punctuation>&type=external,internal`
    * `/api/users/{username}/submissions`
    * `/api/users/{username}/comments/parent_submission`
    * `/api/users?order_by=num_comments/num_submissions/value`

## Usage

```
usage: reddit_crawler.py [-h] [-d DB_NAME] [-t TABLE_PREFIX] [-H HOST]
                         [-u USER] [-s SUBREDDIT] [-p PAGES]

Collect data from Reddit and store in MySQL

optional arguments:
  -h, --help            show this help message and exit
  -d DB_NAME, --database DB_NAME
                        MySQL database where tweets will be stored. Default:
  -t TABLE_PREFIX, --table_prefix TABLE_PREFIX
                        String to be added to beginning of MySQL table names.
                        Default:
  -H HOST, --host HOST  MySQL host. Default: localhost
  -u USER, --user USER  MySQL username. Default: sgiorgi
  -s SUBREDDIT, --subreddit SUBREDDIT
                        . Default: Python
  -p PAGES, --pages PAGES
                        . Default: 10
```

## Dependencies
- [mysqlclient](https://github.com/PyMySQL/mysqlclient-python)
- argparse
- requests
