import asyncio
import pathlib

import aiofiles
import configargparse
import contextvars

from datetime import datetime
from file import write_into_file


def create_parser():
    parser = configargparse.ArgParser(default_config_files=['.env'], ignore_unknown_config_file_keys=True)

    parser.add('-f', '--HISTORY', env_var='HISTORY', help='файл назначения для логов', default='history', type=str, nargs='?')
    parser.add('-c', '--HOST', env_var='HOST', help='хост секретного чата', default='minechat.dvmn.org', type=str, nargs='?')
    parser.add('-p', '--PORT', env_var='PORT', help='порт секретного чата', default=5000, type=int, nargs='?')
    return parser


async def read_from_socket(reader):
    history_file = connections_vars.get().HISTORY
    while True:
        chat_phrase = await reader.readuntil(separator=b'\n')
        if not chat_phrase:
            break
        chat_text = f"{datetime.now().strftime('[%d.%m.%Y %I:%M]')} {chat_phrase.decode('utf-8')}"
        await write_into_file(chat_text, history_file)


async def tcp_echo_client():
    host = connections_vars.get().HOST
    port = connections_vars.get().PORT
    reader, writer = await asyncio.open_connection(host , port)
    await read_from_socket(reader)


def main():
    parser = create_parser()
    options = parser.parse_args()

    connections_vars.set(options)
    try:
        asyncio.run(tcp_echo_client())
    except ConnectionError:
        logging.info(
            'Ошибка соединения, повторное соединение будет через 10 сек.'
        )
    finally:
        asyncio.run(tcp_echo_client())


if __name__ == "__main__":
    connections_vars = contextvars.ContextVar('connections')
    main()
