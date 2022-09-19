from __future__ import print_function

import json
import os

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials


def upload_basic():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    gs_key_file = os.path.dirname(os.path.dirname(__file__)) + "/registration/gsheet_email_key.json"
    if not os.path.isfile(gs_key_file):
        config_file = os.path.dirname(os.path.dirname(__file__)) + "/registration/config.json"
        with open(config_file) as json_file:
            data = json.load(json_file)['email_key']
        with open(gs_key_file, 'w') as fp:
            json.dump(data, fp)

    creds = Credentials.from_service_account_file(gs_key_file, scopes=scope)

    folder_id = '1BcQJKx_OTyKrJ4ZjEFuF8NWDXciwDhZ9'

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': 'photo.jpg', 'parent': [folder_id]}
        media = MediaFileUpload('./GermanVisa/photo.jpg', mimetype='image/jpeg')
        file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
        print('File ID: %s' % file.get('id'))

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


def search_file():
    gs_key_file = os.path.dirname(os.path.dirname(__file__)) + "/registration/gsheet_email_key.json"
    if not os.path.isfile(gs_key_file):
        config_file = os.path.dirname(os.path.dirname(__file__)) + "/registration/config.json"
        with open(config_file) as json_file:
            data = json.load(json_file)['email_key']
        with open(gs_key_file, 'w') as fp:
            json.dump(data, fp)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gs_key_file

    creds, _ = google.auth.default()
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q="mimeType='image/jpeg'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                print(F'Found file: {file.get("name")}, {file.get("id")}')
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None

    return files


if __name__ == '__main__':
    # upload_basic()
    upload_basic()