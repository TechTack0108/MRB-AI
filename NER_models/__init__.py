import spacy
import os
from file_utils import load_data_txt, save_data_txt

nlp_ref = spacy.load("mrb_ref_no_ner_model")
nlp_org = spacy.load("mrb_organizations_ner_model")
nlp_date = spacy.load("mrb_dates_ner_model")


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

try:
    for root, dirs, files in os.walk("../test/extracted_pdf"):
        for file in files:
            # ignore file if it is not a pdf
            if not file.endswith(".txt"):
                print(f"Skipping {file}")
                continue

            file_name = root.split('/')[-1]

            output_file_path_orgs = f"../data/output_data/sender/{file_name}.txt"
            output_file_path_ref_nos = f"../data/output_data/refNo/{file_name}.txt"
            output_file_path_dates = f"../data/output_data/receiveDate/{file_name}.txt"

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
                # if len(nlp_date(file_name).ents) > 0:
                #     date = nlp_date(file_name).ents[0].text
                # else:
                #     date = extract_date(file_text)
                #
                #     if date == "":
                #         date = nlp_date(file_text)
                #         if len(date.ents) > 0:
                #             date = date.ents[0].text

                # Extract the orgs
                orgs = []
                # Check if there is orgs in the file text
                if len(nlp_org(file_text).ents) > 0:
                    for ent in nlp_org(file_text).ents:
                        orgs.append(ent.text)

                if len(orgs) == 0:
                    count_null_files += 1
                else:
                    for content_org in orgs:
                        save_data_txt(output_file_path_orgs, content_org + "\n")

                # print("date", date)

                # Save the data to txt file
                save_data_txt(output_file_path_ref_nos, ref_no)

                # save_data_txt(output_file_path_dates, date)

                print("Finished processing ", file_name)

                count_files += 1
except Exception as e:
    print("File: ", file_name)
    print("Error: ", e)
