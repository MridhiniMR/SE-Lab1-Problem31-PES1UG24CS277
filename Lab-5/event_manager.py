"""Manage event creation, guest registration, and persistence."""

import subprocess
import json
import random
from datetime import date

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create and store an event."""
    if guests is None:
        guests = []

    events[event_name] = {
        "venue": venue,
        "capacity": capacity,
        "guests": guests,
    }
    return events[event_name]


def register_guest(event_name, guest):
    """Register a guest if the event exists and has capacity."""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Return the number of seats remaining for an event."""
    event = events.get(event_name)

    if event is None:
        print("No such event:", event_name)
        return 0

    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Return whether an event is upcoming or completed."""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name, sort_order="name"):
    """Return guest names in the requested sorting order."""
    event = events.get(event_name)

    if event is None:
        print("No such event:", event_name)
        return ""

    if sort_order in ("name", "asc"):
        names = sorted(event["guests"])
    elif sort_order == "desc":
        names = sorted(event["guests"], reverse=True)
    else:
        raise ValueError(
            "sort_order must be 'name', 'asc', or 'desc'"
        )

    return ", ".join(names)


def save_events(file_name="events.json"):
    """Save event data as JSON."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=2)


def load_events(file_name="events.json"):
    """Load event data from JSON."""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            loaded_events = json.load(file)
    except FileNotFoundError:
        print("No saved events file found.")
        return events
    except json.JSONDecodeError:
        print("Saved events file contains invalid JSON.")
        return events

    if not isinstance(loaded_events, dict):
        print("Saved events data has an invalid format.")
        return events

    events.clear()
    events.update(loaded_events)
    return events


def print_badges(event_name):
    """Print badges using the system printing utility."""
    # Helper kept for the lab: not called by the demo
    badge_file = "badges_" + event_name + ".txt"

    try:
        subprocess.run(["lp", badge_file], check=True, shell=False)
    except FileNotFoundError:
        print("Printing utility 'lp' was not found.")
    except subprocess.CalledProcessError:
        print("Badge printing failed.")


def main():
    """Run the event manager demonstration."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop", 2)
    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")
    left = seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))
    print("Tech Meetup guests:", guest_report("Tech Meetup", "name"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))
    guests = events["Tech Meetup"]["guests"]

    if guests:
        winner = random.choice(guests)
        print("Lucky draw winner:", winner)
    else:
        print("No guests available for the lucky draw.")

    save_events()
    restored = load_events()  # reload to confirm the save worked
    print("Events restored from file:", len(restored))
    print("Venues:", [e["venue"] for e in restored.values()])


if __name__ == "__main__":
    main()
