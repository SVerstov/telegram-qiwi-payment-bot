"""
SettingModule
Warning! place api tokens into .env file
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DEBUG = False  # debug mode use sqlite instead postgres
USE_POOLING = True  # if true -> bot will use a pooling method instead webhook

# admin settings
ADMINS = (403196518,)  # telegram_id's

# webhook settings
WEBHOOK_HOST = 'https://yourdomain.com'
WEBHOOK_PATH = '/path/to/webhook'
WEBAPP_HOST = 'localhost'

# logger settings
log_format = r"%(asctime)s [%(levelname)s] %(message)s"
logs_dir = Path('logs')
console_log_level = logging.WARNING

# DB settings
POSTGRES_ENGINE = 'psycopg2'
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

POSTGRES_ENGINE = f'postgresql+{POSTGRES_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}'
