import os
import spacy

from file_utils import load_data_txt, save_data_txt

current_dir = os.path.dirname(os.path.realpath(__file__))
mrb_ai_dir = os.path.dirname(current_dir)

nlp_ref = spacy.load(current_dir + "/mrb_ref_no_ner_model")
nlp_org = spacy.load(current_dir + "/mrb_organizations_ner_model")
nlp_date = spacy.load(current_dir + "/mrb_dates_ner_model")


def extract_ref_no(file_text, file_name):
    # Check if the file name is already a ref no
    if len(nlp_ref(file_name).ents) > 0:
        ref_no = nlp_ref(file_name).ents[0].text
        return ref_no

    # If not, check the text
    # Check if the text contains a ref no
    doc_ref = nlp_ref(file_text)

    if len(doc_ref.ents) > 0:
        ent_ref = doc_ref.ents[0]
        # replace for better formatting
        ref_no = ent_ref.text.replace(
            ".", "").replace(" ", "").replace(" ", "").replace("D", "0").replace("o", "0").replace("O", "")

        return ref_no

    return ""


def extract_orgs(file_text):
    doc_org = nlp_org(file_text)

    if len(doc_org.ents) > 0:
        orgs = []
        for ent in doc_org.ents:
            org = ent.text
            orgs.append(org)
        return orgs

    return []


def extract_date(file_text):
    doc = nlp_date(file_text)

    if len(doc.ents) > 0:
        for ent in doc.ents:
            return ent.text
    else:
        return ""


count_files = 0
count_null_files = 0
file_name = ""

extract_pdf_dir = mrb_ai_dir + "/preprocess/extracted_pdf"

try:
    for root, dirs, files in os.walk(extract_pdf_dir):
        for file in files:
            # ignore file if it is not a pdf
            if not file.endswith(".txt"):
                print(f"Skipping {file}")
                continue

            file_name = root.split('/')[-1]

            output_file_path_orgs = mrb_ai_dir + "/data/output_data/sender/{file_name}.txt"
            output_file_path_ref_nos = mrb_ai_dir + "../data/output_data/refNo/{file_name}.txt"
            output_file_path_dates = mrb_ai_dir + "../data/output_data/receiveDate/{file_name}.txt"

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

                # Extract the ref no
                ref_no = extract_ref_no(file_text, file_name)

                if ref_no == "":
                    ref_no = nlp_ref(file_text)
                    if len(ref_no.ents) > 0:
                        ref_no = ref_no.ents[0].text.replace(".", "").replace(" ", "").replace(" ", "").replace("D",
                                                                                                                "0").replace(
                            "o", "0").replace("O", "")

                # Extract the date
                # Check if there is a date in the file name
                date = extract_date(file_text)
                if date:
                    save_data_txt(output_file_path_dates, date)

                # Extract the orgs
                orgs = []
                # Check if there is orgs in the file text
                if len(nlp_org(file_text).ents) > 0:
                    for ent in nlp_org(file_text).ents:
                        save_data_txt(output_file_path_orgs, ent.text + "\n")
                else:
                    orgs = extract_orgs(file_text)
                    for org in orgs:
                        save_data_txt(output_file_path_orgs, org + "\n")

                print("Finished processing ", file_name)

                count_files += 1
except Exception as e:
    print("File: ", file_name)
    print("Error: ", e)
