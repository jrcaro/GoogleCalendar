import datetime
import os.path
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth import load_credentials_from_file

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def authenticate_google():
    creds, project_id = load_credentials_from_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=SCOPES
    )

    return build("calendar", "v3", credentials=creds)

def main(calendar_id):
  try:
    service = authenticate_google()

    # Call the Calendar API
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI tool to copy Decathlon planning to Google calendar"
    )
    parser.add_argument(
        "--calendar-id", required=True, type=str, help="Google calendar ID"
    )
    
    args = parser.parse_args()
    input = {key: value for key, value in args.__dict__.items() if value is not None}
    main(**input)