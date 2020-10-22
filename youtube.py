from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import client_secrets

class Youtube:
    def __init__(self):
        DEVELOPER_KEY = client_secrets.API_KEY
        YOUTUBE_API_SERVICE_NAME = 'youtube'
        YOUTUBE_API_VERSION = 'v3'
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

    def search(self, search_word):

        # Call the search.list method to retrieve results matching the specified
        # query term.
        try: 
            search_response = self.youtube.search().list(
                q=search_word,
                part='id,snippet',
                maxResults=1
            ).execute()

            videos = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
            for search_result in search_response.get('items', []):
                if search_result['id']['kind'] == 'youtube#video':
                    videos.append('%s' % ("https://www.youtube.com/embed" + search_result['id']['videoId']))

            return videos[0]
        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
        return []       