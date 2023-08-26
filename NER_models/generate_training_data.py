import spacy
import os
import math

from file_utils import load_data_txt, save_data_json

nlp_orgs = spacy.load("mrb_organizations_ner")


# nlp_dates = spacy.load("mrb_dates_ner")
# nlp_refs = spacy.load("mrb_ref_no_ner")
# nlp_subject = spacy.load("mrb_subject_ner")


def test_model(model, text):
    doc = model(text)
    results = []
    entities = []
    for ent in doc.ents:
        entities.append((ent.start_char, ent.end_char, ent.label_))

    if len(entities) > 0:
        results = [text, {"entities": entities}]
    return results


TRAIN_DATA = []
extracted_text_dir = "../preprocess/extracted_pdf"

count_files = 0

try:
    for root, dirs, files in os.walk(extracted_text_dir):
        for file in files:
            count_files += 1

            if not file.endswith(".txt"):
                continue

            file_name = root.split("/")[-1]

            print("processing file: " + file_name)

            file_path = os.path.join(root, file)

            text = load_data_txt(file_path)
            ie_data = {}

            sentences = text.split("\n")

            for sentence in sentences:
                sentence = sentence.strip().replace("\n", " ").replace("\n\n", " ")
                results = test_model(nlp_orgs, sentence)

                if results is not None and results != []:
                    print("results: ", results)
                    TRAIN_DATA.append(results)
                    break

            # print("TRAIN_DATA: ", TRAIN_DATA)

    # save_data_json(
    #     "../data/trained_data/date/mrb_dates_training_data.json", TRAIN_DATA)


except Exception as e:
    print("Error: ", e)

# save_data_json("../data/trained_data/ref_no/mrb_ref_nos_training_data.json", TRAIN_DATA)

save_data_json("../data/trained_data/organizations/mrb_organizations_training_data.json", TRAIN_DATA)

# save_data_json("../data/trained_data/date/mrb_dates_training_data.json", TRAIN_DATA)

# save_data_json("../data/trained_data/subject/mrb_subject_training_data.json", TRAIN_DATA)
print("count_files: ", count_files)
