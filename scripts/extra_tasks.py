from google_helper import get_service

def send_chat_message(space_name, text):
    """Send a message to a Google Chat space."""
    service = get_service('chat', 'v1')
    message = {'text': text}
    result = service.spaces().messages().create(parent=space_name, body=message).execute()
    return f"Message sent to {space_name}. ID: {result.get('name')}"

def list_tasks():
    """List all current tasks."""
    service = get_service('tasks', 'v1')
    results = service.tasks().list(tasklist='@default').execute()
    items = results.get('items', [])
    if not items:
        return "No tasks found."
    return "\n".join([f"- {t['title']} (ID: {t['id']})" for t in items])

def create_task(title, notes=None):
    """Create a new task."""
    service = get_service('tasks', 'v1')
    task = {'title': title, 'notes': notes}
    result = service.tasks().insert(tasklist='@default', body=task).execute()
    return f"Task created: {result.get('title')}"

def get_form_responses(form_id):
    """Retrieve responses from a specific Google Form."""
    # Note: Forms API requires a specific setup, this uses the readonly responses scope
    service = get_service('forms', 'v1')
    result = service.forms().responses().list(formId=form_id).execute()
    responses = result.get('responses', [])
    return f"Found {len(responses)} responses for form {form_id}."

def custom_search(query, search_engine_id):
    """Perform a Google Custom Search."""
    service = get_service('customsearch', 'v1')
    res = service.cse().list(q=query, cx=search_engine_id).execute()
    items = res.get('items', [])
    if not items:
        return "No results found."
    return "\n".join([f"{i['title']}: {i['link']}" for i in items[:3]])

if __name__ == "__main__":
    print("Extra Tasks Script Loaded")
