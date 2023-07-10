import random
import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding

from file_utils import load_data_json, save_data_json


def train_spacy(data, iterations):
    nlp = spacy.blank("en")  # create blank Language class

    # create the built-in pipeline components and add them to the pipeline
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")

    for _, annotations in data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    optimizer = nlp.begin_training()

    for itn in range(iterations):
        print("Start iteration " + str(itn))
        random.shuffle(data)
        losses = {}

        # Create batches of examples
        for texts, annotations in data:
            examples = []
            for i in range(len(texts)):
                examples.append(Example.from_dict(nlp.make_doc(texts[i]), annotations[i]))

            # Update the model with the batch examples
            nlp.update(
                examples,
                drop=0.2,
                sgd=optimizer,
                losses=losses,
            )

        print(losses)
    return nlp


# DATES_TRAIN_DATA = load_data_json("../data/trained_data/date/mrb_dates_training_data.json")
REF_TRAIN_DATA = load_data_json("../data/trained_data/ref_no/mrb_ref_nos_training_data.json")

nlp = train_spacy(REF_TRAIN_DATA, 30)
# nlp.to_disk("mrb_dates_ner_model")
nlp.to_disk("mrb_ref_no_ner_model")
