#!/usr/bin/python

import httplib2
import pprint
import sys
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import AccessTokenCredentials 
from oauth2client import gce

client_id, client_sec = filter(None, open('g_api', 'r').read().split('\n')) 
oauth_scope = 'https://www.googleapis.com/auth/drive'

redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

file_name = sys.argv[1]
credentials = gce.AppAssertionCredentials(scope='https://www.googleapis.com/auth/devstorage.read_write')
http = credentials.authorize(httplib2.Http())
drive_service = build('drive','v2', http=http)

media_body = MediaFileUpload(file_name, mimetype='application/x-tar', resumable=True)
body = {
        'title' : 'Backup init alvolivre.com.br',
        'description' : 'Send backup to google drive',
        'mimeType' : 'application/x-tar'
}

_file = drive_service.files().insert(body=body, media_body=media_body).execute()
