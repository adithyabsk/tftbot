import io
import itertools
import os.path
import json
from pathlib import Path
import random
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseDownload
from bs4 import BeautifulSoup
from markdown import markdown
import logging
from concurrent.futures import ProcessPoolExecutor as Pool

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
GDRIVE_CRED = json.loads(os.environ.get('GDRIVE_CRED'))
GDRIVE_TOKEN = json.loads(os.environ.get('GDRIVE_TOKEN'))
NOTES_FOLDER_ID = os.environ.get("NOTES_FOLDER_ID")
PARENT_FOLDER = Path(__file__).parent
DATA_FOLDER_PATH = (PARENT_FOLDER / "../data").resolve()
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_initial_token():
    flow = InstalledAppFlow.from_client_config(GDRIVE_CRED, SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


def get_service():
    if not os.path.exists('token.json'):
        # seed the token for the first run from the manual client activation
        creds = Credentials.from_authorized_user_info(GDRIVE_TOKEN, SCOPES)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    else:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def print_top_10_files():
    # This function prints 10 most recent files from GDrive and helps debug the
    # flow to setup the GDrive connection.
    service = get_service()
    try:
        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            LOG.info('No files found.')
            return
        LOG.info('Files:')
        for item in items:
            LOG.info(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        LOG.error(f'An error occurred: {error}')


def process_item(items_tuple):
    item, service, dst_folder = items_tuple
    item_name = item['name']
    item_id = item['id']
    item_type = item['mimeType']
    file_path = dst_folder + "/" + item_name

    if item_type == 'application/vnd.google-apps.folder':
        LOG.info("Stepping into folder: {0}".format(file_path))
        download_folder(service, item_id, file_path)  # Recursive call
    elif not item_type.startswith('application/'):
        download_file(service, item_id, file_path)
    else:
        LOG.info("Unsupported file: {0}".format(item_name))


def download_folder(service, folder_id, dst_folder):
    if not os.path.isdir(dst_folder):
        os.mkdir(path=dst_folder)

    results = service.files().list(
        pageSize=300,
        q="parents in '{0}'".format(folder_id),
        fields="files(id, name, mimeType)"
        ).execute()

    items = results.get('files', [])

    items_zip = zip(items, itertools.repeat(service), itertools.repeat(dst_folder))
    with Pool() as pool:
        pool.map(process_item, items_zip)


def download_file(service, fileId, filePath):
    # Note: The parent folders in filePath must exist
    # LOG.info("-> Downloading file with id: {0} name: {1}".format(fileId, filePath))
    request = service.files().get_media(fileId=fileId)
    fh = io.FileIO(filePath, mode='wb')

    try:
        downloader = MediaIoBaseDownload(fh, request, chunksize=1024 * 1024)
        done = False
        while done is False:
            status, done = downloader.next_chunk(num_retries=2)
    finally:
        fh.close()


def download_notes_folder():
    service = get_service()
    download_folder(service, NOTES_FOLDER_ID, str(DATA_FOLDER_PATH))


def get_all_tag_blocks(tag: str) -> List[str]:
    download_notes_folder()
    paths = DATA_FOLDER_PATH.rglob("*.md")
    md_text = '\n'.join(p.read_text() for p in paths)

    html = markdown(md_text)
    lis = BeautifulSoup(html, 'lxml').find_all('li')
    lis_text = [li.next_element.get_text() for li in lis]
    filtered_lis = [li for li in lis_text if "#"+tag in li]

    return filtered_lis


def get_random_tag_block(tag: str) -> str:
    blocks = get_all_tag_blocks(tag)
    return random.choice(blocks)


if __name__ == '__main__':
    tag = "idea"
    print(get_random_tag_block(tag))
