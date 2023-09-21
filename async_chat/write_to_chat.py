import asyncio
import configargparse
import logging
import json

from file import write_into_file
from socket_context_manager import socket_connection


def create_parser():
    parser = configargparse.ArgParser(default_config_files=['.env', 'token.txt'], ignore_unknown_config_file_keys=True)

    parser.add('MESSAGE', help='Текст который нужно отправить в чат', type=str)
    parser.add('-u', '--NAME', env_var='NAME', help='Имя для использования в чате', default='', type=str, nargs='?')
    parser.add('-t', '--TOKEN', env_var='TOKEN', help='Токен для авторизации в чате', default='xxx', type=str, nargs='?')
    parser.add('-c', '--HOST', env_var='HOST', help='Хост секретного чата', default='minechat.dvmn.org', type=str, nargs='?')
    parser.add('-p', '--PORT_TO_WRITE', env_var='PORT_TO_WRITE', help='Порт секретного чата', default=5050, type=int, nargs='?')
    return parser


async def authorise(reader, writer, token):
    writer.write(token.encode())
    await writer.drain()
    data = await reader.readline()
    logger.debug(f'Received: {data.decode()!r}')
    if json.loads(data.decode().split('\n')[0]) is None:
        logger.info('Неизвестный токен. Переключаем на регистрацию.')
        return False
    return True


async def registration(reader, writer, name):
    if not name:
        logging.info('Введите ваше имя')
        name = input()
        name = name.replace('\n', '\\n')
    writer.write(f"{name}\n".encode())
    await writer.drain()
    await reader.readuntil(separator=b'\n')
    data = await reader.readline()
    logger.info(f'Вас зарегистрированы с именем {name}')
    logger.debug(f'Received: {data.decode()}')

    token = "TOKEN=" + json.loads(data.decode().split('\n')[0])['account_hash'] + '\n'
    await write_into_file(token, 'token.txt', mode='w')

    logger.info(
        'Спасибо за регистрацию, ваш токен записан в файл token.txt, перезапустите программу.'
    )
    writer.close()
    await writer.wait_closed()


async def submit_message(reader, writer, message=''):
    data = await reader.readline()
    logger.debug(data.decode())
    message = message.replace('\n', '\\n')
    writer.write(f"{message}\n\n".encode())
    await writer.drain()
    await reader.readline()
    logger.info(f'Сообщение "{message}" отправлено!')


async def chat_connection(options):
    host = options.HOST
    port = options.PORT_TO_WRITE
    token = options.TOKEN
    message = options.MESSAGE
    name = options.NAME

    async with socket_connection(host, port) as socket:

        reader, writer = socket

        data = await reader.readline()
        logger.debug(f'Received: {data.decode()!r}')

        is_token_approve = await authorise(reader, writer, f"{token}\n")

        if not is_token_approve:
            await registration(reader, writer, name)

        await submit_message(reader, writer, message)

        writer.close()
        await writer.wait_closed()


def main():
    logging.basicConfig(
        format='%(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %I:%M:%S %p',
        level=logging.DEBUG
    )

    parser = create_parser()
    options = parser.parse_args()
    logger.debug(options)

    asyncio.run(chat_connection(options))


if __name__ == "__main__":
    logger = logging.getLogger('writer')
    main()
