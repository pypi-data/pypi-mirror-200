# Copyright Formic Technologies 2023
import asyncio
import logging
import sys

from formic_opcua import OpcuaServer

asyncua_logger = logging.getLogger('asyncua')
asyncua_logger.setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(funcName)s:%(lineno)d | %(message)s',
)


def server_exception_handler(loop, context):
    logger.critical(f'Within main server event loop: {context}')
    loop.stop()


def main():
    config_file_path = './example_configs/opcua_config_1.yaml'
    server = OpcuaServer(server_config_file=config_file_path)
    loop = asyncio.new_event_loop()

    # loop = asyncio.get_event_loop()

    try:
        loop.create_task(server.launch())
        loop.set_exception_handler(server_exception_handler)
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(server.stop())
    finally:
        loop.close()


if __name__ == '__main__':
    main()
