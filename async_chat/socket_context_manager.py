import asyncio
import logging
from contextlib import asynccontextmanager


logger = logging.getLogger('socket_connection')


@asynccontextmanager
async def create_socket_connection(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        logger.debug('Соединение открыто')
        yield reader, writer
    except ConnectionResetError:
        logger.debug('Соединение разорвано')
    finally:
        writer.close()
        await writer.wait_closed()
        logger.debug('Соединение закрыто')
