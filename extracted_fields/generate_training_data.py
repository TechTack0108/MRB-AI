from spacy.lang.en import English
import spacy
import os

from file_utils import load_data_txt, save_data_json

nlp = English()
nlp = spacy.load("extracted_fields/mrb_refno_ner")


def test_model(model, text):
    doc = model(text)
    results = []
    entities = []
    for ent in doc.ents:
        entities.append((ent.start_char, ent.end_char, ent.label_))

    if len(entities) > 0:
        results = [text, {"entities": entities}]
    return (results)


TRAIN_DATA = []
extracted_text_dir = "preprocess/extracted_pdf"

try:
    for root, dirs, files in os.walk(extracted_text_dir):
        for file in files:
            file_path = os.path.join(root, file)
            print("file: " + file_path)
            text = load_data_txt(file_path)
            ie_data = {}

            sentences = text.split("\n\n")

            for sentence in sentences:
                sentence = sentence.strip()
                results = test_model(nlp, sentence)

                if results != None and results != []:
                    print("results: ", results)
                    TRAIN_DATA.append(results)

            # print("TRAIN_DATA: ", TRAIN_DATA)

    save_data_json(
        "extracted_fields/data/ref_no/mrb_refnos_training_data.json", TRAIN_DATA)

except Exception as e:
    print("Error: ", e)
