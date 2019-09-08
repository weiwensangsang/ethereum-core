import os

import googleapiclient.discovery
import requests

from googleapiclient.http import MediaFileUpload


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAEfdBhr2EY2z1I7newyVwqFksWjMDjdTY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    print()
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id="UC_x5XG1OV2P6uZZ5FSM9Ttw"
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    r = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UCRr2dbgMHtMq9Z9lbG6GqWA&key=AIzaSyAEfdBhr2EY2z1I7newyVwqFksWjMDjdTY")
    print(r.content)