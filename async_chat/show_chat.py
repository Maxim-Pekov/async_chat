import asyncio
import socket
import configargparse
import logging
from datetime import datetime
from file import write_into_file
from socket_context_manager import socket_connection


RECONNECT_DELAY = 10


def create_parser():
    parser = configargparse.ArgParser(default_config_files=['.env'], ignore_unknown_config_file_keys=True)

    parser.add('-f', '--HISTORY', env_var='HISTORY', help='файл назначения для логов', default='history.txt', type=str, nargs='?')
    parser.add('-c', '--HOST', env_var='HOST', help='хост секретного чата', default='minechat.dvmn.org', type=str, nargs='?')
    parser.add('-p', '--PORT', env_var='PORT', help='порт секретного чата', default=5000, type=int, nargs='?')
    return parser


async def read_from_socket(reader, history_file):
    while True:
        chat_phrase = await reader.readuntil(separator=b'\n')
        if not chat_phrase:
            break
        chat_text = f"{datetime.now().strftime('[%d.%m.%Y %I:%M]')} {chat_phrase.decode('utf-8')}"
        await write_into_file(chat_text, history_file)


async def chat_connection(options):
    host = options.HOST
    port = options.PORT
    history_file = options.HISTORY
    while True:
        try:
            async with socket_connection(host, port) as sock:
                reader, writer = sock
                await read_from_socket(reader, history_file)
        except ConnectionRefusedError:
            logger.info("Соединение с чатом, отсутствует")
        except asyncio.TimeoutError:
            logger.info("Соединение с чатом, отсутствует")
        except socket.gaierror:
            logger.info("Соединение с чатом, отсутствует")
        logger.info(f'Переподключение произойдет через {RECONNECT_DELAY} секунд/ы.')
        await asyncio.sleep(RECONNECT_DELAY)


def main():
    logging.basicConfig(
        format='%(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %I:%M:%S %p',
        level=logging.DEBUG
    )

    parser = create_parser()
    options = parser.parse_args()

    asyncio.run(chat_connection(options))


if __name__ == "__main__":
    logger = logging.getLogger('reader')
    main()
