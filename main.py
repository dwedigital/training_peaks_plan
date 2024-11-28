#!/usr/bin/python3

import icalendar
import os
import requests
from datetime import datetime


def get_calendar():

    # Get the current date and time
    now = datetime.now()

    # Create a new file name with the current date and time
    file_name = "training_peaks_" + now.strftime("%Y%m%d_%H%M%S") + ".ics"

    # Fetch the data from the external URL
    url = "https://www.trainingpeaks.com/ical/3NZQ3FB3XBWUC.ics"
    response = requests.get(url)

    # Write the data to the training_peaks.ics file
    with open(f"{file_name}", "wb") as f:
        f.write(response.content)

    print("New file created:", file_name)


def import_json():
    if not os.path.exists("events.json"):
        return []
    import json

    with open("events.json", "r") as f:
        events = json.load(f)
    return events


def get_events_from_latest_file(events):

    # find all ics files in the current directory
    import glob

    files = glob.glob("*.ics")

    # Read the ics file

    # Create an empty list to store the events

    # Loop through the events in the ics file
    for file in files:
        with open(file, "r") as f:
            cal = icalendar.Calendar.from_ical(f.read())
        for event in cal.walk("vevent"):
            # check if event with uid already exists in events

            for e in events:
                if e["uid"] == event.get("uid"):
                    break
            else:

                # Create a dictionary to store the event details
                event_dict = {}

                # Get the UID of the event
                uid = event.get("uid")

                # Get the start and end times of the event
                start = event.get("dtstart").dt
                end = event.get("dtend").dt

                # Get the summary of the event
                summary = event.get("summary")

                # Get the description of the event
                description = event.get("description")

                # Add the event details to the dictionary
                event_dict["uid"] = uid
                event_dict["start"] = start
                event_dict["end"] = end
                event_dict["summary"] = summary
                event_dict["description"] = description

                # Add the event dictionary to the list of events
                events.append(event_dict)


def write_events_to_json(events):
    # Save the events as a JSON file
    import json

    json = json.dumps(events, indent=4, sort_keys=True, default=str)

    with open("events.json", "w") as f:
        f.write(json)


def write_csv(events):
    import csv

    with open("training_plan.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["UID", "Start", "End", "Summary", "Description"])
        for event in events:
            writer.writerow(
                [
                    event["uid"],
                    event["start"],
                    event["end"],
                    event["summary"],
                    event["description"],
                ]
            )


if __name__ == "__main__":
    get_calendar()
    events = import_json()
    get_events_from_latest_file(events)
    write_events_to_json(events)
    print("Events saved to events.json")
    write_csv(events)
