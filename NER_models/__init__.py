import os
import re
import spacy
import sys

from extract_subject import extract_subject
from file_utils import load_data_txt, save_data_txt

download_id = sys.argv[1]

current_dir = os.path.dirname(os.path.realpath(__file__))
mrb_ai_dir = os.path.dirname(current_dir)

nlp_ref = spacy.load(current_dir + "/mrb_ref_no_ner_model")
nlp_org = spacy.load(current_dir + "/mrb_organizations_ner_model")
nlp_date = spacy.load(current_dir + "/mrb_dates_ner_model")


def extract_ref_no(file_text, file_name):
    doc_ref = nlp_ref(file_name)
    ref_nos = []

    if len(doc_ref.ents) > 0:
        ref_nos.append(doc_ref.ents[0].text)

    doc_ref = nlp_ref(file_text)

    for ent in doc_ref.ents:
        ref = ent.text
        # check if the ref is in the list of ref_nos, and the ref contains only letters and numbers and "-" and "_"
        if ref not in ref_nos and re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?!.*\s)[a-zA-Z\d_-]+$', ref):
            ref_nos.append(ref)

    return ref_nos


def check_if_value_exist_in_dict(value, dict):
    for values in dict:
        if value in values:
            return True


def extract_orgs(file_text, file_name):
    try:
        org_dict = {
            "CSL": ["COLAS"],
            "CSR": ["COLAS"],
            "HGU": ["HUYNDAI", "GHELLA"],
            "DLM": ["DAELIM"],
            "HNC": ["HANOCORP"],
            "VC2": ["VINACONEX"],
            "PSC": ["POSCO"],
            "UJV": ["ALSTOM", "COLAS", "THALES", "SAS"],
            "MRB": [""]
        }

        orgs = []
        # find the org in the file name first
        doc_org = nlp_org(file_text)

        if len(doc_org.ents) > 0:
            for ent in doc_org.ents:
                org = ent.text.upper()

                # check if the org is in the org_dict, if it is, replace it with the org in the file name
                if "(" + org + ")" in orgs or org in orgs or any(char.isdigit() for char in org) or any(
                        char in "!@#$%^&*[]{};:,./<>?\|`~-=_+" for char in org) or any(
                    char in "ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ" for char in
                    org):
                    continue
                else:
                    found = False
                    # replace the org in the org_dict with the org in the file name. ex: orgs = ["POSCO", "HNC"]
                    # and the org is "PSC".Replace "POSCO" with "PSC"
                    if org in org_dict and org not in orgs:
                        for i, organization in enumerate(orgs):
                            if organization in org_dict[org]:
                                orgs[i] = org
                                found = True

                    # if the org is in the values array of the org_dict, and the key is in the orgs array, continue
                    for key in org_dict:
                        if org in org_dict[key] and key in orgs:
                            found = True

                    if not found:
                        orgs.append(org)

        return orgs
    except Exception as e:
        print(e)


def extract_subject_file(file_text):
    file_subject = extract_subject(file_text)

    print("file_subject: ", file_subject)

    if file_subject:
        return file_subject
    else:
        return ""


def extract_date(file_text, file_name):
    doc = nlp_date(file_name)

    if len(doc.ents) == 0:
        doc = nlp_date(file_text)

    if len(doc.ents) > 0:
        if "%" in doc.ents[0].text and "&*" in doc.ents[0].text:
            doc.ents[0].text.replace("%", "").replace("&*", "")

        return doc.ents[0].text

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
                date = extract_date(file_text, file_name)

                if date:
                    save_data_txt(output_file_path_dates, date)

                # Extract the orgs
                orgs = extract_orgs(file_text, file_name)

                for org in orgs:
                    save_data_txt(output_file_path_orgs, org + "\n")

                # Extract the subject
                subject = extract_subject_file(file_text)
                save_data_txt(output_file_path_subject, subject)

                print("Finished processing ", file_name)

                count_files += 1

except Exception as e:
    print("File: ", file_name)
    print("Error: ", e)
