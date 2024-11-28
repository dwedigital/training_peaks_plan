#!/usr/bin/python3

from postmarker.core import PostmarkClient
import json
from datetime import datetime, timedelta
import csv
import pytz


# open the events.json and only get the events that are today and in the future


def future_events():
    # open the events.json

    with open("events.json", "r") as f:
        events = json.load(f)

    # get the current date and time

    now = datetime.now().replace(tzinfo=pytz.utc)

    # create an empty list to store the events
    future_events = []

    # loop through the events
    for event in events:
        # check if the event is today or or 7 days in the future
        if datetime.fromisoformat(event["start"]).replace(
            tzinfo=pytz.utc
        ) >= now and datetime.fromisoformat(event["start"]).replace(
            tzinfo=pytz.utc
        ) <= now + timedelta(
            days=7
        ):
            future_events.append(event)

    # write the events to a csv called upcoiming_events.csv

    with open("week_plan.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["UID", "Start", "End", "Summary", "Description"])
        for event in future_events:
            writer.writerow(
                [
                    event["uid"],
                    event["start"],
                    event["end"],
                    event["summary"],
                    event["description"],
                ]
            )


def send_email():
    postmark = PostmarkClient(server_token="d99f61fd-5670-4571-8161-87cfab849886")
    email = postmark.emails.Email(
        From="dave@dwedigital.com",
        To=["dave@dwedigital.com", "thlwhipp@hotmail.co.uk"],
        Subject="Next week's running plan",
        HtmlBody="Please find attached the plan for next week",
        TextBody="Please find attached the plan for next week",
    )

    # attach the binary contents of events.csv to the email

    email.attach_binary(open("week_plan.csv", "rb").read(), "week_plan.csv")
    email.send()
    timetsamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Email sent - {timetsamp}")


if __name__ == "__main__":
    future_events()
    send_email()
