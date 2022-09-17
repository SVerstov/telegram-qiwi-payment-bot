from create_bot import launch_bot
from db.db_utils import update_blacklist
from logger import setup_logger
from handlers import register_handlers


def main():
    setup_logger()
    register_handlers()
    update_blacklist()
    launch_bot()


if __name__ == '__main__':
    main()
