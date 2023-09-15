import asyncio
import pathlib

import aiofiles
import configargparse
import contextvars

from datetime import datetime


def create_parser():
    parser = configargparse.ArgParser(default_config_files=['.env'])

    parser.add('-f', '--FILE', env_var='FILE', help='файл назначения для логов', default='history', type=str, nargs='?')
    parser.add('-c', '--HOST', env_var='HOST', help='хост секретного чата', default='minechat.dvmn.org', type=str, nargs='?')
    parser.add('-p', '--PORT', env_var='PORT', help='порт секретного чата', default=5000, type=int, nargs='?')
    return parser


async def write_into_file(chat_phrase):
    # pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(connections_vars.get().FILE, mode='a') as f:
        chat_text = f"{datetime.now().strftime('[%d.%m.%Y %I:%M]')} {chat_phrase}"
        await f.write(chat_text)
        print(chat_text)


async def read_from_socket(reader):
    while True:
        chat_phrase = await reader.read(512)
        if not chat_phrase:
            break
        await write_into_file(chat_phrase.decode("utf-8"))


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        connections_vars.get().HOST, connections_vars.get().PORT)
    await read_from_socket(reader)


def main():
    parser = create_parser()
    options = parser.parse_args()

    connections_vars.set(options)
    asyncio.run(tcp_echo_client())


if __name__ == "__main__":
    connections_vars = contextvars.ContextVar('host')
    main()
