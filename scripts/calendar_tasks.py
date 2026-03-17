import datetime
from google_helper import get_service

def check_daily_availability():
    """
    Check for events today and return open slots.
    """
    service = get_service('calendar', 'v3')
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_of_day = (datetime.datetime.utcnow().replace(hour=23, minute=59, second=59)).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=end_of_day, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return "You are free for the rest of the day."

    schedule = []
    for idx, event in enumerate(events, start=1):
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'Untitled event')
        schedule.append(f"{idx}. {start}: {summary} (ID: {event.get('id')})")

    return "\n".join(schedule)

def schedule_followup(summary, minutes=30):
    """
    Schedule a followup meeting.
    """
    service = get_service('calendar', 'v3')
    start_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(minutes=minutes)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat() + 'Z'},
        'end': {'dateTime': end_time.isoformat() + 'Z'},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return f"Event created: {event.get('htmlLink')}"

def list_calendars():
    """List all calendars for the user."""
    service = get_service('calendar', 'v3')
    results = service.calendarList().list().execute()
    calendars = results.get('items', [])
    if not calendars:
        return "No calendars found."
    return "\n".join([f"{c['summary']} (ID: {c['id']})" for c in calendars])

def create_generic_event(summary, start_time, end_time, description=None, calendar_id='primary'):
    """Create an event with specific times and details."""
    service = get_service('calendar', 'v3')
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_time},
        'end': {'dateTime': end_time},
    }
    result = service.events().insert(calendarId=calendar_id, body=event).execute()
    return f"Created event: {result.get('htmlLink')}"

def list_events_range(calendar_id='primary', time_min=None, time_max=None):
    """List calendar events between two specific ISO timestamps."""
    service = get_service('calendar', 'v3')
    results = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max, singleEvents=True, orderBy='startTime').execute()
    events = results.get('items', [])
    if not events:
        return f"No events found for calendar {calendar_id} in the requested range."
    return "\n".join([f"{e['start'].get('dateTime', e['start'].get('date'))}: {e['summary']} (ID: {e['id']})" for e in events])

def create_event_with_meet(summary, start_time, end_time):
    """Create a calendar event with a Google Meet link."""
    service = get_service('calendar', 'v3')
    event = {
        'summary': summary,
        'start': {'dateTime': start_time},
        'end': {'dateTime': end_time},
        'conferenceData': {
            'createRequest': {
                'requestId': f"meet-{datetime.datetime.now().timestamp()}",
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }
    result = service.events().insert(
        calendarId='primary', 
        body=event, 
        conferenceDataVersion=1
    ).execute()
    meet_link = result.get('hangoutLink') or result.get('htmlLink')
    return f"Event with Meet created: {meet_link}"

if __name__ == "__main__":
    print("Calendar Task Script Loaded")
