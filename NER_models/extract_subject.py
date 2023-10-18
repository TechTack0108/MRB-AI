import re


def extract_subject(text):
    # Define a pattern to match the subject
    pattern = r"(?:Về việc|Subject:|Chủ đề:)\s*(.*?)(?=\n\w+:|\n\n|\n\d+\.)"

    # Search for the pattern in the text
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL | re.UNICODE)

    if match:
        subject = match.group(1).strip().lstrip(": ")
        return subject.replace('\n', ' ')
    else:
        return None
