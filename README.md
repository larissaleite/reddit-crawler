# reddit-crawler-mysql

Fork of [reddit-crawler](https://github.com/larissaleite/reddit-crawler):
- Works with MySQL database instead of SQLite
- `MySQLDatabase` class added
- Added argparse
- Separated defaults into a separate py file: `app/defaults.py`

## Installation

Run `pip install -r requirements.txt`

## Examples

Collect 1 page of data from the "Python" subreddit and put in the MySQL database `code`. MySQL table names begin with `python_`.

```bash
python reddit_crawler.py -d code -s python
```

Collect 10 pages of data from the "The_Donald" subreddit and put in the MySQL database `politics`. MySQL table names begin with `repub_`.

```bash
python reddit_crawler.py -d politics -t repub -p 10 -s the_donald
```

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
  -u USER, --user USER  MySQL username. Default: 
  -s SUBREDDIT, --subreddit SUBREDDIT
                        Name of subreddit to search. Default: Python
  -p PAGES, --pages PAGES
                        Number of pages to search. Default: 10
```

## Dependencies
- [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)
- argparse
- requests
