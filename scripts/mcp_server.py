from mcp.server.fastmcp import FastMCP
import os
from starlette.requests import Request
from starlette.responses import JSONResponse

# Import all modular task scripts
import gmail_tasks
import calendar_tasks
import calendar_detailed_tasks
import drive_tasks
import drive_detailed_tasks
import chat_tasks
import editor_tasks
import task_tasks
import form_tasks
import extra_tasks
from google_helper import get_credentials

mcp = FastMCP("Google Workspace")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check for Docker / load balancers."""
    return JSONResponse({"status": "ok", "service": "google-workspace-mcp"})


@mcp.tool()
async def google_auth_setup() -> str:
  """
  Initialize Google OAuth for this workspace.

  When you run this tool the first time after selecting
  `google_workspace`, it will open the Google consent window
  and store a local token so other tools (Gmail, Drive, etc.)
  can use the account without asking again.
  """
  # This call blocks until the OAuth browser flow completes.
  get_credentials()
  return "Google Workspace OAuth completed successfully."

@mcp.tool()
async def workspace_capabilities() -> str:
    """
    Get a guide on what this Google Workspace agent can do.
    Call this if the user asks what features are available or for help.
    """
    return """
    I can manage your entire Google Workspace:
    - GMAIL: Search, Read, Send, Mark Read/Unread, Archive, Forward, and Labels.
    - CALENDAR: List agenda, Schedule, Meet links, Secondary Calendars, Update, and Delete.
    - DRIVE: Search, Upload, Share, Copy, Move, Folders, Empty Trash, and Revisions.
    - SHEETS: Read data, Append rows, Clear ranges, and Manage Tabs.
    - DOCS: Create, Read text, Append content, and Search/Replace text.
    - SLIDES: Create, Read all text, and Add slides.
    - FORMS: Create, Get responses, Update titles, and Add Questions.
    - TASKS: List tasks, Create, Complete, Delete, and Manage TaskLists.
    - SEARCH: Use Google Custom Search for web/internal data.
    """

# --- 1. GMAIL TOOLS ---
@mcp.tool()
async def gmail_search(query: str = "is:unread"):
    """
    Search Gmail. Use operators like 'from:name@example.com', 'subject:urgent', or 'after:2024/01/01'.
    Returns a list of matching message IDs and snippets.
    """
    return gmail_tasks.search_urgent_emails(query)

@mcp.tool()
async def gmail_send_message(to: str, subject: str, message: str):
    """
    Send an email. 
    'to' must be a valid email address. 
    'message' is the body text.
    """
    return gmail_tasks.send_email(to, subject, message)

@mcp.tool()
async def gmail_label_management(email_id: str, label: str, action: str = "add"):
    """Tag an email with a label (e.g. 'URGENT', 'PROJECT')."""
    return gmail_tasks.manage_labels(email_id, label, action)

@mcp.tool()
async def gmail_read_full(email_id: str):
    """Read full content of an email."""
    return gmail_tasks.get_email_body(email_id)

@mcp.tool()
async def gmail_trash(email_id: str):
    """Move an email to the trash."""
    return gmail_tasks.delete_email(email_id)

@mcp.tool()
async def gmail_list_labels():
    """List all Gmail labels organized by the user."""
    return gmail_tasks.list_labels()

@mcp.tool()
async def gmail_get_conversation(thread_id: str):
    """Retrieve all messages in a conversation thread."""
    return gmail_tasks.get_thread(thread_id)

@mcp.tool()
async def gmail_mark_read(message_id: str, read: bool = True):
    """Mark an email as read or unread."""
    if read:
        return gmail_tasks.mark_as_read(message_id)
    return gmail_tasks.mark_as_unread(message_id)

@mcp.tool()
async def gmail_draft_operations(action: str, to: str = "", subject: str = "", body: str = ""):
    """Manage drafts: 'list' or 'create'."""
    if action == "list":
        return gmail_tasks.list_drafts()
    return gmail_tasks.create_draft(to, subject, body)

@mcp.tool()
async def gmail_archive(email_id: str):
    """Archive an email (removes from Inbox)."""
    return gmail_tasks.archive_email(email_id)

@mcp.tool()
async def gmail_forward(email_id: str, to: str):
    """Forward an email to another address."""
    return gmail_tasks.forward_email(email_id, to)

@mcp.tool()
async def gmail_trash_empty():
    """Wipe out all items in Gmail Trash permanently."""
    return gmail_tasks.empty_gmail_trash()

# --- 2. DRIVE TOOLS ---
@mcp.tool()
async def drive_search(query: str = "name contains 'Project'"):
    """Search for any file or folder in Google Drive."""
    return drive_tasks.find_files(query)

@mcp.tool()
async def drive_trash_empty():
    """Wipe out all items in the Drive Trash permanently."""
    return drive_detailed_tasks.empty_drive_trash()

@mcp.tool()
async def drive_upload(file_path: str):
    """Upload a local file to Google Drive."""
    return drive_detailed_tasks.upload_file_item(file_path)

@mcp.tool()
async def drive_share(file_id: str, email: str, role: str = 'reader'):
    """Share a file with an authorized email. role: 'reader', 'commenter', or 'writer'."""
    return drive_detailed_tasks.share_drive_file(file_id, email, role)

@mcp.tool()
async def drive_copy_file(file_id: str, new_name: str = None):
    """Create a copy of an existing file."""
    return drive_detailed_tasks.copy_file(file_id, new_name)

@mcp.tool()
async def drive_get_details(file_id: str):
    """Get all technical metadata and properties of a file."""
    return drive_detailed_tasks.get_file_metadata(file_id)

@mcp.tool()
async def drive_revisions_list(file_id: str):
    """List all past versions/revisions of a specific file."""
    return drive_detailed_tasks.list_file_revisions(file_id)

@mcp.tool()
async def drive_move_file(file_id: str, folder_id: str):
    """Move a file to a different folder ID."""
    return drive_detailed_tasks.move_file_to(file_id, folder_id)

@mcp.tool()
async def drive_create_folder(name: str, parent_id: str = None):
    """Create a new folder in Google Drive."""
    return drive_detailed_tasks.create_folder(name, parent_id)

# --- 3. CHAT TOOLS ---
@mcp.tool()
async def chat_message(space_id: str, text: str):
    """Send a message to a Google Chat space or DM."""
    return extra_tasks.send_chat_message(space_id, text)

@mcp.tool()
async def chat_manage_space(action: str, name: str = ""):
    """Manage Chat spaces (list, create). Action: 'list' or 'create'."""
    if action == "list":
        return chat_tasks.list_chat_spaces()
    return chat_tasks.create_chat_space(name)

@mcp.tool()
async def chat_membership(action: str, space_name: str, email: str = ""):
    """Manage space members: 'list' or 'add'."""
    if action == "list":
        return chat_tasks.list_members(space_name)
    return chat_tasks.add_member(space_name, email)

@mcp.tool()
async def chat_message_history(space_name: str):
    """Read the message history/recent messages in a space."""
    return chat_tasks.list_messages(space_name)

@mcp.tool()
async def chat_edit_message(message_name: str, new_text: str):
    """Edit a message that was previously sent."""
    return chat_tasks.update_message(message_name, new_text)

@mcp.tool()
async def chat_react(message_name: str, emoji: str):
    """Add an emoji reaction to a message."""
    return chat_tasks.add_reaction(message_name, emoji)

# --- 4, 5, 6. EDITOR TOOLS (DOCS, SHEETS, SLIDES) ---
@mcp.tool()
async def editor_create(type: str, title: str):
    """Create a new 'doc', 'sheet', or 'slide'."""
    if type == "doc":
        return editor_tasks.create_doc(title)
    elif type == "slide":
        return editor_tasks.create_slide_deck(title)
    return "Use drive tools for generic creation."

@mcp.tool()
async def doc_read_content(doc_id: str):
    """Read full text content from a Google document."""
    return editor_tasks.get_doc_text(doc_id)

@mcp.tool()
async def sheets_read(spreadsheet_id: str, range_name: str = "Sheet1!A:Z"):
    """Read data from a Google Spreadsheet."""
    return editor_tasks.get_sheet_data(spreadsheet_id, range_name)

@mcp.tool()
async def slide_add_page(presentation_id: str):
    """Add a new slide to a presentation."""
    return editor_tasks.add_slide_to_deck(presentation_id, "", "")

@mcp.tool()
async def sheets_append_data(spreadsheet_id: str, values: list):
    """Append a row of data to a spreadsheet."""
    return drive_tasks.update_log_sheet(spreadsheet_id, "Sheet1!A:Z", values)

@mcp.tool()
async def doc_append_text(doc_id: str, text: str):
    """Add text to the very end of a Google Doc."""
    return editor_tasks.append_doc_content(doc_id, text)

@mcp.tool()
async def sheets_clear(spreadsheet_id: str, range_name: str):
    """Wipe data from a specific range in a spreadsheet."""
    return editor_tasks.clear_spreadsheet_range(spreadsheet_id, range_name)

@mcp.tool()
async def sheets_tabs_list(spreadsheet_id: str):
    """List all sheets/tabs inside a spreadsheet."""
    return editor_tasks.list_sheet_tabs(spreadsheet_id)

@mcp.tool()
async def sheets_tabs_manage(action: str, spreadsheet_id: str, tab_title: str = "", sheet_id: str = ""):
    """Create or delete sheets (tabs). Action: 'create' or 'delete'."""
    if action == "create":
        return editor_tasks.create_sheet_tab(spreadsheet_id, tab_title)
    elif action == "delete":
        return editor_tasks.delete_sheet_tab(spreadsheet_id, sheet_id)
    return "Action not recognized."

@mcp.tool()
async def slides_pages_list(presentation_id: str):
    """Get the total count of slides in a presentation."""
    return editor_tasks.list_slide_pages(presentation_id)

@mcp.tool()
async def slides_read_content(presentation_id: str):
    """Read all text content from all slides/pages in a presentation."""
    return editor_tasks.get_slides_text(presentation_id)

@mcp.tool()
async def doc_search_replace(doc_id: str, find: str, replace: str):
    """Search and replace text throughout a Google Doc."""
    return editor_tasks.search_replace_doc_text(doc_id, find, replace)


# --- 7. CALENDAR TOOLS ---
@mcp.tool()
async def calendar_manage(action: str, summary: str = "", event_id: str = "", start_time: str = "", end_time: str = "", calendar_id: str = "primary"):
    """
    Manage calendar: 'list' (agenda), 'list_all' (calendars), 'create', 'update', or 'delete'.
    """
    if action == "list":
        return calendar_tasks.check_daily_availability()
    elif action == "list_all":
        return calendar_tasks.list_calendars()
    elif action == "create":
        if start_time and end_time:
            return calendar_tasks.create_generic_event(summary, start_time, end_time, None, calendar_id)
        return calendar_tasks.schedule_followup(summary)
    elif action == "update":
        return calendar_detailed_tasks.update_calendar_event(event_id, summary, None, start_time, end_time, calendar_id)
    elif action == "delete":
        return calendar_detailed_tasks.delete_calendar_event(event_id, calendar_id)
    elif action == "list_range":
        return calendar_tasks.list_events_range(calendar_id, start_time, end_time)
    elif action == "create_meet":
        return calendar_tasks.create_event_with_meet(summary, start_time, end_time)
    return "Action not recognized."

@mcp.tool()
async def calendar_secondary_manage(action: str, name: str = "", description: str = "", calendar_id: str = ""):
    """Manage secondary calendars: 'create' or 'delete'."""
    if action == "create":
        return calendar_detailed_tasks.create_secondary_calendar(name, description)
    elif action == "delete":
        return calendar_detailed_tasks.delete_secondary_calendar(calendar_id)
    return "Action not recognized."

# --- 8. FORM TOOLS ---
@mcp.tool()
async def forms_manage(action: str, title: str = "", form_id: str = "", questions: list = None):
    """Manage Forms: 'create', 'add_questions', 'get_info', 'update_title', or 'responses'."""
    if action == "create":
        return form_tasks.create_form(title)
    elif action == "add_questions":
        return form_tasks.add_questions_to_form(form_id, questions)
    elif action == "get_info":
        return form_tasks.get_form_metadata(form_id)
    elif action == "update_title":
        return form_tasks.update_form_title(form_id, title)
    return form_tasks.list_form_responses(form_id)

# --- 9. CUSTOM SEARCH ---
@mcp.tool()
async def web_search_internal(query: str):
    """Use Google Custom Search to find web or internal results."""
    return extra_tasks.custom_search(query, os.getenv('GOOGLE_SEARCH_ID'))

# --- 10. TASK TOOLS ---
@mcp.tool()
async def tasks_action(action: str, title: str = "", task_id: str = ""):
    """Manage Tasks: 'list', 'create', 'complete', or 'delete'."""
    if action == "list":
        return extra_tasks.list_tasks()
    elif action == "create":
        return task_tasks.create_task_item(title)
    elif action == "complete":
        return task_tasks.complete_task_item(task_id)
    elif action == "delete":
        return task_tasks.delete_task_item(task_id)
    elif action == "list_lists":
        return task_tasks.list_tasklists()
    elif action == "manage_lists":
        # New nested logic for lists themselves
        # action is 'manage_lists', so we check another param? 
        # Better to just use 'action' as 'create_list' or 'delete_list' in list_lists.
        return "Use specific actions for list management."
    elif action == "create_list":
        return task_tasks.create_task_list(title)
    elif action == "delete_list":
        return task_tasks.delete_task_list(task_id) # using task_id as tasklist_id for consistency
    return "Action not recognized."

if __name__ == "__main__":
    import os
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport in ("http", "streamable-http"):
        mcp.settings.host = "0.0.0.0"
        mcp.settings.port = int(os.getenv("MCP_PORT", "8000"))
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")
