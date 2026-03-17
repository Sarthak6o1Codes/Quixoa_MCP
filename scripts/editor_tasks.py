from google_helper import get_service

def create_doc(title):
    """Create a new Google Doc."""
    service = get_service('docs', 'v1')
    doc = service.documents().create(body={'title': title}).execute()
    return f"Created Doc: {doc.get('title')} (ID: {doc.get('documentId')})"

def update_doc_content(doc_id, text):
    """Insert text at the beginning of a Google Doc."""
    service = get_service('docs', 'v1')
    requests = [{'insertText': {'location': {'index': 1}, 'text': text}}]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    return f"Updated Doc: {doc_id}"

def create_slide_deck(title):
    """Create a new Google Slides presentation."""
    service = get_service('slides', 'v1')
    presentation = service.presentations().create(body={'title': title}).execute()
    return f"Created Presentation: {presentation.get('title')} (ID: {presentation.get('presentationId')})"

def update_spreadsheet(spreadsheet_id, range_name, values):
    """Specific tool for updating existing cells in Sheets."""
    service = get_service('sheets', 'v4')
    body = {'values': values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    updated = result.get('updatedCells', 0)
    return f"Updated {updated} cells in {spreadsheet_id} at range {range_name}."
def get_doc_text(doc_id):
    """Read the full text content of a Google Doc."""
    service = get_service('docs', 'v1')
    doc = service.documents().get(documentId=doc_id).execute()
    content = doc.get('body').get('content')
    text = ""
    for element in content:
        if 'paragraph' in element:
            for text_run in element.get('paragraph').get('elements'):
                text += text_run.get('textRun', {}).get('content', '')
    return text

def add_slide_to_deck(presentation_id, title, subtitle):
    """Add a new slide to an existing presentation."""
    service = get_service('slides', 'v1')
    requests = [
        {'createSlide': {}},
        {'insertText': {'objectId': 'p', 'text': title}} # This is simplified
    ]
    # For a clinical assistant, we'll keep it simple: adding a blank slide
    service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': [{'createSlide': {}}]}).execute()
    return f"New slide added to presentation {presentation_id}"

def get_sheet_data(spreadsheet_id, range_name):
    """Read data or lists from Google Sheets in a readable table format."""
    service = get_service('sheets', 'v4')
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    if not values:
        return f"No data found in range {range_name} for sheet {spreadsheet_id}."

    lines = []
    for row_idx, row in enumerate(values, start=1):
        row_str = ", ".join(str(cell) for cell in row)
        lines.append(f"{row_idx}: {row_str}")

    return "\n".join(lines)

def append_doc_content(doc_id, text):
    """Append text to the end of a Google Doc."""
    service = get_service('docs', 'v1')
    doc = service.documents().get(documentId=doc_id).execute()
    # Find the end of the document
    end_index = doc.get('body').get('content')[-1].get('endIndex')
    requests = [{'insertText': {'location': {'index': end_index - 1}, 'text': text}}]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    return f"Appended text to Doc: {doc_id}"

def clear_spreadsheet_range(spreadsheet_id, range_name):
    """Clear all data from a specific range in Sheets."""
    service = get_service('sheets', 'v4')
    service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name, body={}).execute()
    return f"Cleared range {range_name} in Sheet {spreadsheet_id}"

def list_sheet_tabs(spreadsheet_id):
    """List all tabs (sheets) in a spreadsheet."""
    service = get_service('sheets', 'v4')
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])
    return "\n".join([s.get('properties').get('title') for s in sheets])

def list_slide_pages(presentation_id):
    """List all slides in a presentation."""
    service = get_service('slides', 'v1')
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    if not slides:
        return f"Presentation {presentation_id} has no slides."
    return "\n".join([f"Slide {idx}" for idx, _slide in enumerate(slides, start=1)])

def search_replace_doc_text(doc_id, find_text, replace_text):
    """Search and replace all occurrences of text in a Doc."""
    service = get_service('docs', 'v1')
    requests = [
        {
            'replaceAllText': {
                'containsText': {'text': find_text, 'matchCase': False},
                'replaceText': replace_text,
            }
        }
    ]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    return f"Replaced all '{find_text}' with '{replace_text}' in Doc {doc_id}"

def create_sheet_tab(spreadsheet_id, tab_title):
    """Add a new empty sheet (tab) to a spreadsheet."""
    service = get_service('sheets', 'v4')
    request = {'addSheet': {'properties': {'title': tab_title}}}
    result = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [request]}).execute()
    return f"Added tab '{tab_title}' to sheet {spreadsheet_id}"

def delete_sheet_tab(spreadsheet_id, sheet_id):
    """Delete a tab from a spreadsheet using its sheetId."""
    service = get_service('sheets', 'v4')
    request = {'deleteSheet': {'sheetId': sheet_id}}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [request]}).execute()
    return f"Deleted tab with ID {sheet_id} from spreadsheet {spreadsheet_id}"

def get_slides_text(presentation_id):
    """Read all text content from all slides in a presentation."""
    service = get_service('slides', 'v1')
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    text = ""
    for i, slide in enumerate(slides):
        text += f"\n--- Slide {i+1} ---\n"
        for element in slide.get('pageElements', []):
            if 'shape' in element and 'text' in element['shape']:
                for text_run in element['shape']['text'].get('textElements', []):
                    if 'textRun' in text_run:
                        text += text_run['textRun'].get('content', '')
    return text

if __name__ == "__main__":
    print("Editor Tasks Script Loaded")
