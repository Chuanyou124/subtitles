from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

CLIENT_SECRETS_FILE = '/Users/isaac/Documents/proj/util/subtitles/test/client_secret.json'

SCOPES = 'https://www.googleapis.com/auth/youtube.force-ssl'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
YOUTUBE = discovery.build('youtube', 'v3', http=creds.authorize(Http()))
print(YOUTUBE)

def process(vid):
    caption_info = YOUTUBE.captions().list(
            part='id', videoId=vid).execute().get('items', [])
    caption_str = YOUTUBE.captions().download(
            id=caption_info[0]['id'], tfmt='srt').execute()
    caption_data = caption_str.split('\n\n')
    for line in caption_data:
        if line.count('\n') > 1:
            i, cap_time, caption = line.split('\n', 2)
            print('%02d) [%s] %s' % (
                    int(i), cap_time, ' '.join(caption.split())))

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        VID = sys.argv[1]
    process(VID)
