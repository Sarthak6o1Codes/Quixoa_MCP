from google_helper import get_service

def get_calendar_metadata(calendar_id='primary'):
    """Get metadata for a specific calendar."""
    service = get_service('calendar', 'v3')
    calendar = service.calendars().get(calendarId=calendar_id).execute()
    return (
        f"Calendar: {calendar.get('summary', 'Untitled')}\n"
        f"ID: {calendar.get('id')}\n"
        f"Timezone: {calendar.get('timeZone', 'Unknown')}\n"
        f"Description: {calendar.get('description', 'No description')}"
    )

def delete_calendar_event(event_id, calendar_id='primary'):
    """Permanently delete an event."""
    service = get_service('calendar', 'v3')
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    return f"Deleted event: {event_id}"

def share_calendar(calendar_id, user_email, role='reader'):
    """Share a calendar with another user."""
    service = get_service('calendar', 'v3')
    rule = {
        'scope': {'type': 'user', 'value': user_email},
        'role': role
    }
    result = service.acl().insert(calendarId=calendar_id, body=rule).execute()
    return f"Shared {calendar_id} with {user_email} (Role: {role})"

def update_calendar_event(event_id, summary=None, description=None, start_time=None, end_time=None, calendar_id='primary'):
    """Reschedule or update an existing event."""
    service = get_service('calendar', 'v3')
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    
    if summary: event['summary'] = summary
    if description: event['description'] = description
    if start_time: event['start'] = {'dateTime': start_time}
    if end_time: event['end'] = {'dateTime': end_time}
    
    updated_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
    return f"Event updated: {updated_event.get('htmlLink')}"

def create_secondary_calendar(name, description=None):
    """Create a new secondary calendar."""
    service = get_service('calendar', 'v3')
    calendar = {'summary': name, 'description': description}
    result = service.calendars().insert(body=calendar).execute()
    return f"Created calendar: {result.get('summary')} (ID: {result.get('id')})"

def delete_secondary_calendar(calendar_id):
    """Delete a secondary calendar."""
    service = get_service('calendar', 'v3')
    service.calendars().delete(calendarId=calendar_id).execute()
    return f"Deleted calendar: {calendar_id}"

if __name__ == "__main__":
    print("Calendar Detailed Tasks Loaded")
