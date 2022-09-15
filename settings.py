import logging
from pathlib import Path

# logger settings
log_format = r"%(asctime)s [%(levelname)s] %(message)s"
info_log_file= Path('logs/info.log')
warnings_log_file= Path('logs/warnings.log')
console_log_level = logging.WARNING
