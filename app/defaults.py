import getpass, os

# reddit defaults
BASE_URL = 'https://www.reddit.com/'
DEFAULT_PAGES = 1
DEFAULT_SUB_REDDIT = 'Python'

# mysql defaults
DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))+'/db/'
DEFAULT_DB = ''
DEFAULT_TABLE_PREFIX = ''
DEFAULT_HOST = 'localhost'
DEFAULT_USER = getpass.getuser()

# other
DEF_LIMIT = 10