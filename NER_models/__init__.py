import os
import re
import sys
import spacy

from file_utils import load_data_txt, save_data_txt

download_id = sys.argv[1]

current_dir = os.path.dirname(os.path.realpath(__file__))
mrb_ai_dir = os.path.dirname(current_dir)

nlp_ref = spacy.load(current_dir + "/mrb_ref_no_ner_model")
nlp_org = spacy.load(current_dir + "/mrb_organizations_ner_model")
nlp_date = spacy.load(current_dir + "/mrb_dates_ner_model")
nlp_subject = spacy.load(current_dir + "/mrb_subject_ner_model")


def extract_ref_no(file_text, file_name):
    doc_ref = nlp_ref(file_name)
    ref_nos = []

    if len(doc_ref.ents) > 0:
        ref_nos.append(doc_ref.ents[0].text)

    doc_ref = nlp_ref(file_text)

    for ent in doc_ref.ents:
        ref = ent.text
        # check if the ref is in the list of ref_nos, and the ref contains both letters and numbers
        if ref not in ref_nos and (bool(re.search(r'[a-zA-Z]', ref)) and bool(re.search(r'\d', ref))):
            ref_nos.append(ref)

    return ref_nos


def extract_orgs(file_text):
    doc_org = nlp_org(file_text)
    orgs = []

    if len(doc_org.ents) > 0:
        for ent in doc_org.ents:
            org = ent.text
            # check if the org lowercase, uppercase and org is in the list of orgs
            if org.lower() not in orgs and org.upper() not in orgs and org not in orgs:
                orgs.append(org)

    return orgs


def extract_subject(file_text):
    doc_subject = nlp_subject(file_text)
    subject = ""

    if len(doc_subject.ents) > 0:
        for ent in doc_subject.ents:
            subject = ent.text
            break

    return subject


def extract_date(file_text):
    doc = nlp_date(file_text)

    if len(doc.ents) > 0:
        return doc.ents[0].text
    else:
        return ""


count_files = 0
count_null_files = 0
file_name = ""

extract_pdf_dir = mrb_ai_dir + "/preprocess/extracted_pdf/" + download_id

try:
    for root, dirs, files in os.walk(extract_pdf_dir):
        for file in files:
            # ignore file if it is not a pdf
            if not file.endswith("page_1.txt"):
                continue

            file_name = root.split('/')[-1]

            output_file_path_orgs = mrb_ai_dir + f"/data/output_data/sender/{file_name}.txt"
            output_file_path_ref_nos = mrb_ai_dir + f"/data/output_data/refNo/{file_name}.txt"
            output_file_path_dates = mrb_ai_dir + f"/data/output_data/receiveDate/{file_name}.txt"
            output_file_path_subject = mrb_ai_dir + f"/data/output_data/subject/{file_name}.txt"

            if os.path.exists(output_file_path_ref_nos):
                continue
            else:
                print("Processing", file)
                file_text = load_data_txt(os.path.join(root, file))

                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(output_file_path_ref_nos), exist_ok=True)
                os.makedirs(os.path.dirname(output_file_path_orgs), exist_ok=True)
                os.makedirs(os.path.dirname(
                    output_file_path_dates), exist_ok=True)
                os.makedirs(os.path.dirname(
                    output_file_path_subject), exist_ok=True)

                # Extract the ref no
                ref_nos_list = extract_ref_no(file_text, file_name)

                for ref in ref_nos_list:
                    save_data_txt(output_file_path_ref_nos, ref + "\n")

                # Extract the date
                # Check if there is a date in the file name
                date = extract_date(file_text)
                print("Date: ", date)

                if date:
                    save_data_txt(output_file_path_dates, date)

                # Extract the orgs
                orgs = extract_orgs(file_text)

                for org in orgs:
                    save_data_txt(output_file_path_orgs, org + "\n")

                # Extract the subject
                # subject = extract_subject(file_text)
                # if subject:
                #     save_data_txt(output_file_path_subject, subject)

                print("Finished processing ", file_name)

                count_files += 1
except Exception as e:
    print("File: ", file_name)
    print("Error: ", e)
