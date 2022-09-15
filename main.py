import logging

from create_bot import launch_bot
from logger import setup_logger
from handlers import register_handlers


def main():
    setup_logger()
    register_handlers()
    launch_bot()



if __name__ == '__main__':
    main()
