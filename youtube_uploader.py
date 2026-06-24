import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import datetime
import json
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("Error: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, or YOUTUBE_REFRESH_TOKEN environment variables not set.")
        return None

    credentials = Credentials(
        token=None,  # Access token will be refreshed
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token"
    )

    try:
        return googleapiclient.discovery.build(
            "youtube", "v3", credentials=credentials)
    except Exception as e:
        print(f"Error building YouTube service: {e}")
        return None

def upload_video(
    youtube_service,
    file_path,
    title,
    description,
    tags,
    category_id,
    privacy_status="private",
    scheduled_date=None,
    thumbnail_path=None
):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    if scheduled_date:
        # YouTube API expects ISO 8601 format
        body["status"]["publishAt"] = scheduled_date.isoformat() + ".000Z"
        body["status"]["privacyStatus"] = "private" # Must be private before scheduling

    insert_request = youtube_service.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    print(f"Uploading video: {title}...")
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f"Uploaded {int(status.resumable_progress * 100)}%")

    print(f"Video upload complete. Video ID: {response["id"]}")

    if thumbnail_path and os.path.exists(thumbnail_path):
        print(f"Uploading thumbnail: {thumbnail_path}")
        thumbnail_insert_request = youtube_service.thumbnails().set(
            videoId=response["id"],
            media_body=googleapiclient.http.MediaFileUpload(thumbnail_path)
        )
        thumbnail_insert_request.execute()
        print("Thumbnail uploaded.")

    return response

if __name__ == "__main__":
    # This script is intended to be called by a GitHub Action.
    # It expects environment variables for YouTube API credentials and video metadata.
    youtube_service = get_authenticated_service()
    if youtube_service:
        video_path = os.environ.get("YOUTUBE_VIDEO_PATH")
        video_title = os.environ.get("YOUTUBE_TITLE")
        video_description = os.environ.get("YOUTUBE_DESCRIPTION")
        video_tags = os.environ.get("YOUTUBE_TAGS")
        thumbnail_path = os.environ.get("YOUTUBE_THUMBNAIL_PATH")
        scheduled_publish_at = os.environ.get("YOUTUBE_SCHEDULED_PUBLISH_AT")

        if not all([video_path, video_title, video_description, video_tags]):
            print("Error: Missing required environment variables for YouTube upload.")
            exit(1)

        scheduled_date_obj = None
        if scheduled_publish_at:
            try:
                scheduled_date_obj = datetime.datetime.fromisoformat(scheduled_publish_at.replace("Z", "+00:00"))
            except ValueError:
                print(f"Warning: Invalid scheduled_publish_at format: {scheduled_publish_at}. Uploading as private immediately.")
                scheduled_date_obj = None

        upload_video(
            youtube_service,
            video_path,
            video_title,
            video_description,
            video_tags.split(","),
            "28", # Default category ID for Science & Technology
            privacy_status="private" if scheduled_date_obj else "public", # Default to public if not scheduled
            scheduled_date=scheduled_date_obj,
            thumbnail_path=thumbnail_path
        )
