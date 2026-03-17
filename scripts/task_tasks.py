from google_helper import get_service

def create_task_item(title, notes=None, due=None):
    """Create a new task in the default list."""
    service = get_service('tasks', 'v1')
    task = {'title': title, 'notes': notes, 'due': due}
    result = service.tasks().insert(tasklist='@default', body=task).execute()
    return f"Task created: {result.get('title')}"

def delete_task_item(task_id):
    """Delete a task."""
    service = get_service('tasks', 'v1')
    service.tasks().delete(tasklist='@default', task=task_id).execute()
    return f"Deleted task: {task_id}"

def complete_task_item(task_id):
    """Mark a task as completed."""
    service = get_service('tasks', 'v1')
    task = service.tasks().get(tasklist='@default', task=task_id).execute()
    task['status'] = 'completed'
    service.tasks().update(tasklist='@default', task=task_id, body=task).execute()
    return f"Completed task: {task_id}"

def list_tasklists():
    """List all available task lists."""
    service = get_service('tasks', 'v1')
    results = service.tasklists().list().execute()
    items = results.get('items', [])
    return "\n".join([f"{t['title']} (ID: {t['id']})" for t in items])

def create_task_list(title):
    """Create a new Task List."""
    service = get_service('tasks', 'v1')
    result = service.tasklists().insert(body={'title': title}).execute()
    return f"Created task list: {result.get('title')} (ID: {result.get('id')})"

def delete_task_list(tasklist_id):
    """Delete a Task List."""
    service = get_service('tasks', 'v1')
    service.tasklists().delete(tasklist=tasklist_id).execute()
    return f"Deleted task list: {tasklist_id}"

if __name__ == "__main__":
    print("Task Module Script Loaded")
