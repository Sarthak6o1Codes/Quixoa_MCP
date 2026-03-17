from google_helper import get_service

def create_form(title):
    """Create a new Google Form."""
    service = get_service('forms', 'v1')
    form = {'info': {'title': title}}
    result = service.forms().create(body=form).execute()
    return f"Created Form: {result.get('info').get('title')} (ID: {result.get('formId')})"

def get_form_metadata(form_id):
    """Get descriptive details of a form."""
    service = get_service('forms', 'v1')
    result = service.forms().get(formId=form_id).execute()
    info = result.get('info', {})
    return (
        f"Form Title: {info.get('title', 'Untitled')}\n"
        f"Form ID: {result.get('formId', form_id)}\n"
        f"Description: {info.get('description', 'No description')}"
    )

def list_form_responses(form_id):
    """Readable list of all responses for a form."""
    service = get_service('forms', 'v1')
    result = service.forms().responses().list(formId=form_id).execute()
    responses = result.get('responses', [])

    if not responses:
        return f"No responses found for form {form_id}."

    lines = []
    for idx, resp in enumerate(responses, start=1):
        ts = resp.get('lastSubmittedTime') or resp.get('createTime') or 'unknown time'
        answers = resp.get('answers', {})
        flat_answers = []
        for answer in answers.values():
            text_answers = answer.get('textAnswers', {}).get('answers', [])
            values = [item.get('value', '') for item in text_answers if item.get('value')]
            if values:
                flat_answers.append(", ".join(values))
        preview = "; ".join(flat_answers)[:160] or "No readable text answers"
        lines.append(f"{idx}. Submitted at {ts} - {preview}")

    return "\n".join(lines)

def update_form_title(form_id, new_title):
    """Update the title of a Google Form."""
    service = get_service('forms', 'v1')
    update = {
        'requests': [{
            'updateFormInfo': {
                'info': {'title': new_title},
                'updateMask': 'title'
            }
        }]
    }
    service.forms().batchUpdate(formId=form_id, body=update).execute()
    return f"Updated form {form_id} title to {new_title}"

def add_questions_to_form(form_id, questions):
    """
    Add multiple choice or text questions to a form.
    'questions' should be a list of dicts: [{'type': 'text', 'title': 'Your Name'}, {'type': 'choice', 'title': 'Fav Color', 'options': ['Red', 'Blue']}]
    """
    service = get_service('forms', 'v1')
    requests = []
    index = 0
    for q in questions:
        new_item = {
            'createItem': {
                'item': {
                    'title': q['title'],
                    'questionItem': {
                        'question': {
                            'required': True,
                        }
                    }
                },
                'location': {'index': index}
            }
        }
        if q['type'] == 'choice':
            new_item['createItem']['item']['questionItem']['question']['choiceQuestion'] = {
                'type': 'RADIO',
                'options': [{'value': v} for v in q.get('options', [])]
            }
        else:
            new_item['createItem']['item']['questionItem']['question']['textQuestion'] = {}
        
        requests.append(new_item)
        index += 1

    service.forms().batchUpdate(formId=form_id, body={'requests': requests}).execute()
    return f"Successfully added {len(questions)} questions to form {form_id}."

if __name__ == "__main__":
    print("Form Tasks Script Loaded")
