import logging
from pathlib import Path

# Warning! place API_TOKEN into .env file
DEBUG = False
USE_POOLING = True  # if true -> bot will use a pooling method instead webhook

# admin settings
admins = ('leshm',)  # username or telegram_id

# webhook settings
WEBHOOK_HOST = 'https://yourdomain.com'
WEBHOOK_PATH = '/path/to/webhook'
WEBAPP_HOST = 'localhost'

# logger settings
log_format = r"%(asctime)s [%(levelname)s] %(message)s"
info_log_file = Path('logs/info.log')
warnings_log_file = Path('logs/warnings.log')
console_log_level = logging.WARNING

# billing
lifetime = 5

# DB settings
POSTGRES_ENGINE = 'psycopg2'
POSTGRES_DB = 'dbname'
POSTGRES_USER = 'user'
POSTGRES_PASSWORD = 'hardpass'
POSTGRES_HOST = 'db'
POSTGRES_PORT = 5432

POSTGRES_ENGINE = f'postgresql+{POSTGRES_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}'
