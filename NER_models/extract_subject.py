import re


def extract_subject(text):
    pattern = r"(?:Về việc|Ve việc|Viv|ve viec|Subject|subject|Chủ đề|chu de|Ve viec|Chu de|VỀ vige)\s*:\s*([^:\n]+.*?)(?=\n\w+:|$)(?![^\n]*\n[^\w:]+)"

    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL | re.UNICODE)

    if match:
        subject = match.group(1).strip()
        return subject.replace('\n', ' ')
    else:
        return None
