import asyncio
import pathlib

import aiofiles
import configargparse
import contextvars
import logging
import json


def create_parser():
    parser = configargparse.ArgParser(default_config_files=['.env', 'token.txt'], ignore_unknown_config_file_keys=True)

    parser.add('MESSAGE', help='Текст который нужно отправить в чат', type=str)
    parser.add('-u', '--NAME', env_var='NAME', help='Имя для использования в чате', default='', type=str, nargs='?')
    parser.add('-t', '--TOKEN', env_var='TOKEN', help='Токен для авторизации в чате', default='', type=str, nargs='?')
    parser.add('-c', '--HOST', env_var='HOST', help='Хост секретного чата', default='minechat.dvmn.org', type=str, nargs='?')
    parser.add('-p', '--PORT', env_var='PORT', help='Порт секретного чата', default=5050, type=int, nargs='?')
    return parser


async def authorise(reader, writer, token):
    writer.write(token.encode())
    await writer.drain()
    data = await reader.readline()
    logging.debug(f'Received: {data.decode()!r}')
    if json.loads(data.decode().split('\n')[0]) is None:
        logging.info('Неизвестный токен. Переключаем на регистрацию.')
        return False
    return True


async def registration(reader, writer):
    name = connection_details.get().NAME
    if not name:
        logging.info(f'Введите ваше имя')
        name = input()
        name = name.replace('\n', '\\n')
    writer.write(f"{name}\n".encode())
    await writer.drain()
    await reader.readuntil(separator=b'\n')
    data = await reader.readline()
    logging.info(f'Вас зарегистрированы с именем {name}')
    logging.debug(f'Received: {data.decode()}')
    async with aiofiles.open('token.txt', mode='w') as file:
        token = "TOKEN=" + json.loads(data.decode().split('\n')[0])['account_hash']+'\n'
        await file.write(token)
        logging.debug(f'token: {token}')
    writer.close()
    await writer.wait_closed()


async def submit_message(reader, writer, message=''):
    data = await reader.readline()
    logging.debug(data.decode())

    writer.write(f"{message}\n\n".encode())
    await writer.drain()
    await reader.readline()
    logging.info(f'Сообщение "{message}" отправлено!')


async def tcp_echo_client():
    host = connection_details.get().HOST
    port = connection_details.get().PORT
    token = connection_details.get().TOKEN
    message = connection_details.get().MESSAGE

    reader, writer = await asyncio.open_connection(host, port)

    data = await reader.readline()
    logging.debug(f'Received: {data.decode()!r}')

    is_token_approve = await authorise(reader, writer, f"{token}\n")

    if not is_token_approve:
        await registration(reader, writer)

    await submit_message(reader, writer, message)

    logging.info('Соединение закрыто')
    writer.close()
    await writer.wait_closed()


def main():
    logging.basicConfig(
        format='%(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %I:%M:%S %p',
        level=logging.INFO
    )

    parser = create_parser()
    options = parser.parse_args()
    logging.debug(options)

    connection_details.set(options)

    try:
        asyncio.run(tcp_echo_client())
    except ConnectionResetError:
        logging.info(
            f'Спасибо за регистрацию, ваш токен записан в файл token.txt, перезапустите программу.'
        )


if __name__ == "__main__":
    connection_details = contextvars.ContextVar('connection_details')
    logger = logging.getLogger('writer')
    main()
