import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import client_secrets

DEVELOPER_KEY = client_secrets.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=options.max_results
    ).execute()

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s) (%s)' % (search_result['snippet']['title'], "https://www.youtube.com/watch?v=" + search_result['id']['videoId'], search_result['snippet']['thumbnails']['medium']['url']))

    print('Videos:\n', '\n'.join(videos), '\n')


if __name__ == '__main__':
    search_term = "get lucky - daft punk"

    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default=search_term)
    parser.add_argument('--max-results', help='Max results', default=1)
    args = parser.parse_args()

    try:
        youtube_search(args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))