import random
import spacy
from spacy.training.example import Example

from file_utils import load_data_json, save_data_json


def train_spacy(data, iterations):
    TRAIN_DATA = data
    nlp = spacy.blank("en")  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")

    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    optimizer = nlp.begin_training()
    for itn in range(iterations):
        print("Start iteration " + str(itn))
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update(
                [example],
                drop=0.5,
                sgd=optimizer,
                losses=losses,
            )
        print(losses)
    return (nlp)


TRAIN_DATA = load_data_json(
    "extracted_fields/data/ref_no/mrb_refnos_training_data.json")

nlp = train_spacy(TRAIN_DATA, 30)
nlp.to_disk("extracted_fields/mrb_refnos_ner_model")
