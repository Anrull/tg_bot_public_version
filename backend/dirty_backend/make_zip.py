import zipfile
import os
import asyncio


async def zip_files():
    with zipfile.ZipFile('time_files/Files_by_Anloss.zip', 'w') as zipf:
        for root, _, files in os.walk('Books'):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, 'Books'))
        for root, _, files in os.walk("dicts"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, 'dicts'))
                

async def made_zip_files_logs():
    with zipfile.ZipFile('time_files/logs.zip', 'w') as zipf:
        for root, _, files in os.walk('logs'):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, 'logs'))


if __name__ == "__main__":
    asyncio.run(zip_files())
    asyncio.run(made_zip_files_logs())