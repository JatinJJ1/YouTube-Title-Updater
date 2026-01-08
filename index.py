import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_youtube_service():
    token_info = json.loads(os.environ["TOKEN_JSON"])

    credentials = Credentials.from_authorized_user_info(
        token_info, SCOPES
    )
    return build("youtube", "v3", credentials=credentials)

def update_title(video_id):
    youtube = get_youtube_service()

    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    item = response["items"][0]

    views = item["statistics"]["viewCount"]
    snippet = item["snippet"]

    old_title = snippet["title"]
    description = snippet["description"]
    category_id = snippet["categoryId"]

    new_title = f"This Video Has About {views} Views (Probably)"

    if new_title == old_title:
        print("Title already up to date. No change.")
        return

    youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": new_title,
                "description": description,
                "categoryId": category_id
            }
        }
    ).execute()

    print("Title updated to:", new_title)

if __name__ == "__main__":
    VIDEO_ID = "ayEPAbXWxEA"
    update_title(VIDEO_ID)


