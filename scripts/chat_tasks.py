from google_helper import get_service

def create_chat_space(display_name):
    """Create a new Google Chat space."""
    service = get_service('chat', 'v1')
    space = {'display_name': display_name, 'space_type': 'SPACE'}
    result = service.spaces().create(body=space).execute()
    return f"Created space: {result.get('name')}"

def list_chat_spaces():
    """List all available Google Chat spaces."""
    service = get_service('chat', 'v1')
    result = service.spaces().list().execute()
    spaces = result.get('spaces', [])
    if not spaces:
        return "No Chat spaces found."
    return "\n".join([f"{s['displayName']} ({s['name']})" for s in spaces])

def delete_chat_message(message_name):
    """Delete a specific message in Google Chat."""
    service = get_service('chat', 'v1')
    service.spaces().messages().delete(name=message_name).execute()
    return f"Deleted message: {message_name}"

def add_reaction(message_name, emoji_name):
    """Add a reaction to a Chat message."""
    service = get_service('chat', 'v1')
    reaction = {'emoji': {'unicode': emoji_name}}
    result = service.spaces().messages().reactions().create(parent=message_name, body=reaction).execute()
    return f"Added reaction to {message_name}"

def list_members(space_name):
    """List all members in a Chat space."""
    service = get_service('chat', 'v1')
    result = service.spaces().members().list(parent=space_name).execute()
    memberships = result.get('memberships', [])
    if not memberships:
        return f"No members found for {space_name}."

    lines = []
    for idx, membership in enumerate(memberships, start=1):
        member = membership.get('member', {})
        lines.append(
            f"{idx}. {member.get('displayName', member.get('name', 'Unknown member'))} "
            f"({member.get('type', 'UNKNOWN')})"
        )
    return "\n".join(lines)

def add_member(space_name, user_email):
    """Add a new member to a Chat space."""
    service = get_service('chat', 'v1')
    membership = {'member': {'name': f'users/{user_email}', 'type': 'HUMAN'}}
    result = service.spaces().members().create(parent=space_name, body=membership).execute()
    return f"Added {user_email} to space {space_name}"

def list_messages(space_name):
    """List recent messages in a space."""
    service = get_service('chat', 'v1')
    result = service.spaces().messages().list(parent=space_name).execute()
    messages = result.get('messages', [])
    if not messages:
        return f"No recent messages found for {space_name}."

    lines = []
    for idx, message in enumerate(messages[:10], start=1):
        sender = message.get('sender', {}).get('displayName', 'Unknown sender')
        text = (message.get('text') or '').strip() or '[No text content]'
        lines.append(f"{idx}. {sender}: {text}")
    return "\n".join(lines)

def update_message(message_name, new_text):
    """Edit an existing message."""
    service = get_service('chat', 'v1')
    message = {'text': new_text}
    result = service.spaces().messages().patch(name=message_name, body=message, updateMask="text").execute()
    return f"Updated message: {result.get('name')}"

if __name__ == "__main__":
    print("Chat Tasks Script Loaded")
