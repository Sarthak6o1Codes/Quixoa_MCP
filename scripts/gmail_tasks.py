from google_helper import get_service

def search_urgent_emails(query="label:unread urgent"):
    """
    Search for urgent unread emails and return a short, readable summary.
    """
    service = get_service('gmail', 'v1')
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        return f"No messages found for query: '{query}'."

    lines = []
    for idx, msg in enumerate(messages[:5], start=1):  # Limit to 5 for safety
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        lines.append(f"{idx}. ID: {msg['id']} — {txt.get('snippet', '').strip()}")

    return "\n".join(lines)

def draft_reply(email_id, body):
    """
    Draft a reply for a specific email.
    """
    service = get_service('gmail', 'v1')
    message = {
        'message': {
            'threadId': email_id,
            'raw': '' # In a real implementation, you'd construct a base64 encoded RFC822 message
        }
    }
import base64
from email.message import EmailMessage

def send_email(to, subject, body):
    """Send a real email immediately."""
    service = get_service('gmail', 'v1')
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}
    result = service.users().messages().send(userId='me', body=create_message).execute()
    return f"Email sent to {to}. ID: {result.get('id')}"

def manage_labels(email_id, label_name, action='add'):
    """Add or remove a label (like 'URGENT' or 'PROCESSED') to an email."""
    service = get_service('gmail', 'v1')
    body = {'addLabelIds': [label_name]} if action == 'add' else {'removeLabelIds': [label_name]}
    service.users().messages().modify(userId='me', id=email_id, body=body).execute()
    return f"Label {label_name} {action}ed to email {email_id}"

def get_email_body(email_id):
    """Read the full content of an email (not just the snippet)."""
    service = get_service('gmail', 'v1')
    message = service.users().messages().get(userId='me', id=email_id, format='full').execute()
    
    # Simple extraction of the text body for the AI
    import base64
    payload = message.get('payload', {})
    parts = payload.get('parts', [])
    body = "No text content found."
    
    if not parts:
        data = payload.get('body', {}).get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode()
    else:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part.get('body', {}).get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode()
                break
    
    return body

def delete_email(email_id):
    """Move an email to the Trash folder."""
    service = get_service('gmail', 'v1')
    service.users().messages().trash(userId='me', id=email_id).execute()
    return f"Email {email_id} has been moved to the trash."

def list_labels():
    """List all Gmail labels."""
    service = get_service('gmail', 'v1')
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    return "\n".join([f"{l['name']} (ID: {l['id']})" for l in labels])

def get_thread(thread_id):
    """Retrieve a full conversation thread."""
    service = get_service('gmail', 'v1')
    thread = service.users().threads().get(userId='me', id=thread_id).execute()
    messages = thread.get('messages', [])
    if not messages:
        return f"No messages found in thread {thread_id}."

    lines = []
    for idx, message in enumerate(messages, start=1):
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h.get('value') for h in headers if h.get('name') == 'Subject'), 'No subject')
        sender = next((h.get('value') for h in headers if h.get('name') == 'From'), 'Unknown sender')
        snippet = message.get('snippet', '').strip()
        lines.append(f"{idx}. From: {sender} | Subject: {subject} | {snippet}")
    return "\n".join(lines)

def mark_as_read(message_id):
    """Remove 'UNREAD' label from an email."""
    service = get_service('gmail', 'v1')
    body = {'removeLabelIds': ['UNREAD']}
    service.users().messages().modify(userId='me', id=message_id, body=body).execute()
    return f"Message {message_id} marked as read."

def mark_as_unread(message_id):
    """Add 'UNREAD' label to an email."""
    service = get_service('gmail', 'v1')
    body = {'addLabelIds': ['UNREAD']}
    service.users().messages().modify(userId='me', id=message_id, body=body).execute()
    return f"Message {message_id} marked as unread."

def list_drafts():
    """List all email drafts."""
    service = get_service('gmail', 'v1')
    results = service.users().drafts().list(userId='me').execute()
    drafts = results.get('drafts', [])
    if not drafts:
        return "You have no drafts."

    lines = []
    for idx, draft in enumerate(drafts, start=1):
        draft_id = draft.get('id')
        msg = draft.get('message', {})
        snippet = msg.get('snippet', '')
        lines.append(f"{idx}. Draft ID: {draft_id} — {snippet}")

    return "\n".join(lines)

def create_draft(to, subject, body):
    """Create a new email draft."""
    service = get_service('gmail', 'v1')
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft_body = {'message': {'raw': encoded_message}}
    result = service.users().drafts().create(userId='me', body=draft_body).execute()
    return f"Draft created with ID: {result.get('id')}"

def archive_email(message_id):
    """Archive an email by removing it from the Inbox."""
    service = get_service('gmail', 'v1')
    body = {'removeLabelIds': ['INBOX']}
    service.users().messages().modify(userId='me', id=message_id, body=body).execute()
    return f"Email {message_id} archived."

def forward_email(message_id, to_email):
    """Forward an email to another recipient."""
    service = get_service('gmail', 'v1')
    # First get the message details
    msg = service.users().messages().get(userId='me', id=message_id, format='raw').execute()
    import base64
    from email.message import EmailMessage
    import email
    
    raw_msg = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mime_msg = email.message_from_bytes(raw_msg)
    
    new_msg = EmailMessage()
    new_msg['To'] = to_email
    new_msg['From'] = 'me'
    new_msg['Subject'] = f"Fwd: {mime_msg['Subject']}"
    new_msg.set_content(f"---------- Forwarded message ---------\nFrom: {mime_msg['From']}\nDate: {mime_msg['Date']}\nSubject: {mime_msg['Subject']}\nTo: {mime_msg['To']}\n\n{get_email_body(message_id)}")
    
    encoded_message = base64.urlsafe_b64encode(new_msg.as_bytes()).decode()
    create_message = {'raw': encoded_message}
    service.users().messages().send(userId='me', body=create_message).execute()
    return f"Email {message_id} forwarded to {to_email}."

def empty_gmail_trash():
    """Permanently delete all messages currently in the Trash."""
    service = get_service('gmail', 'v1')
    # Use delete on the trash folder? Actually Gmail API has a direct way?
    # No, you have to find messages in TRASH and delete them or use a batch.
    # Actually, people usually want to just "empty trash".
    # There is no single "empty trash" endpoint for messages, you'd list and delete.
    # But wait, there is `service.users().messages().batchDelete`.
    # Let's just do a simple list and delete for now.
    results = service.users().messages().list(userId='me', q='label:TRASH').execute()
    messages = results.get('messages', [])
    if not messages:
        return "Trash is already empty."
    for msg in messages:
        service.users().messages().delete(userId='me', id=msg['id']).execute()
    return f"Deleted {len(messages)} messages from trash."

if __name__ == "__main__":
    print("Gmail Task Script Loaded")
