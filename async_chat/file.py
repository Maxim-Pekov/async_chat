import aiofiles


async def write_into_file(message, file_name, mode='a'):
    async with aiofiles.open(file_name, mode=mode) as f:
        print(message)
        await f.write(message)
