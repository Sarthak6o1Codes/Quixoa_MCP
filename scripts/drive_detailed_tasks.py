from google_helper import get_service

def search_files(query):
    """General purpose Drive search with readable summary."""
    service = get_service('drive', 'v3')
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])
    if not files:
        return f"No Drive files matched query: '{query}'."

    lines = [
        f"{idx}. {f['name']} (ID: {f['id']}, Type: {f['mimeType']})"
        for idx, f in enumerate(files, start=1)
    ]
    return "\n".join(lines)

def delete_file_permanently(file_id):
    """Delete a file from Drive permanently."""
    service = get_service('drive', 'v3')
    service.files().delete(fileId=file_id).execute()
    return f"Deleted file: {file_id}"

def upload_file_item(file_path, mime_type='application/octet-stream'):
    """Upload a local file to Drive."""
    from googleapiclient.http import MediaFileUpload
    service = get_service('drive', 'v3')
    file_metadata = {'name': file_path.split('/')[-1]}
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return f"Uploaded File ID: {file.get('id')}"

def share_drive_file(file_id, user_email, role='reader'):
    """Share a medical record or file with an authorized user email."""
    service = get_service('drive', 'v3')
    permission = {
        'type': 'user',
        'role': role,
        'emailAddress': user_email
    }
    service.permissions().create(fileId=file_id, body=permission).execute()
    return f"Successfully shared file {file_id} with {user_email} (Role: {role})"

def copy_file(file_id, new_name=None):
    """Create a copy of a file."""
    service = get_service('drive', 'v3')
    body = {'name': new_name} if new_name else {}
    result = service.files().copy(fileId=file_id, body=body).execute()
    return f"Created copy: {result.get('name')} (ID: {result.get('id')})"

def get_file_metadata(file_id):
    """Retrieve key metadata for a specific file in a readable format."""
    service = get_service('drive', 'v3')
    result = service.files().get(
        fileId=file_id,
        fields="id, name, mimeType, createdTime, modifiedTime, owners, webViewLink",
    ).execute()

    owner_names = ", ".join([o.get("emailAddress", "") for o in result.get("owners", [])])
    return (
        f"Name: {result.get('name')}\n"
        f"ID: {result.get('id')}\n"
        f"Type: {result.get('mimeType')}\n"
        f"Owners: {owner_names or 'Unknown'}\n"
        f"Created: {result.get('createdTime')}\n"
        f"Modified: {result.get('modifiedTime')}\n"
        f"Open in browser: {result.get('webViewLink')}"
    )

def move_file_to(file_id, new_parent_id):
    """Move a file into a specific folder."""
    service = get_service('drive', 'v3')
    # Retrieve the existing parents to remove
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents', []))
    # Move the file to the new folder
    file = service.files().update(fileId=file_id,
                                    addParents=new_parent_id,
                                    removeParents=previous_parents,
                                    fields='id, parents').execute()
    return f"Moved file to folder {new_parent_id}"

def create_folder(folder_name, parent_id=None):
    """Create a new folder in Google Drive."""
    service = get_service('drive', 'v3')
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
    result = service.files().create(body=file_metadata, fields='id').execute()
    return f"Created folder {folder_name} (ID: {result.get('id')})"

def empty_drive_trash():
    """Permanently delete all items currently in the user's trash."""
    service = get_service('drive', 'v3')
    service.files().emptyTrash().execute()
    return "Google Drive trash has been emptied."

def list_file_revisions(file_id):
    """List all previous versions (revisions) of a file."""
    service = get_service('drive', 'v3')
    results = service.revisions().list(fileId=file_id).execute()
    revisions = results.get('revisions', [])
    return "\n".join([f"ID: {r['id']}, Modified: {r['modifiedTime']}" for r in revisions])

if __name__ == "__main__":
    print("Drive Detailed Tasks Loaded")
