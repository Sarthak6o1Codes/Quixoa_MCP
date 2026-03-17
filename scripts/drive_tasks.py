from google_helper import get_service

def find_files(query="name contains 'Project'"):
    """
    Search for files in Drive with a specific query.
    """
    service = get_service('drive', 'v3')
    results = service.files().list(
        q=query,
        pageSize=10, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        return "No items found matching the query."
    
    return "\n".join([f"{item['name']} (ID: {item['id']}, Type: {item['mimeType']})" for item in items])

def update_log_sheet(spreadsheet_id, range_name, values):
    """
    Append a row to a spreadsheet log.
    """
    service = get_service('sheets', 'v4')
    body = {'values': [values]}
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    return f"{result.get('updates').get('updatedCells')} cells updated."

if __name__ == "__main__":
    print("Drive Task Script Loaded")
