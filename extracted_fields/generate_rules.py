from file_utils import load_data_json, save_data_json
from spacy.lang.en import English


def generate_better_organization_patterns(file):
    data = load_data_json(file)

    better_version = data

    # apppend lowercase, camelcase of each organization
    for org in list(data):
        print("in loop")
        better_version.append(org.lower())
        better_version.append(org.title())

        # append lowercase, camelcase of each organization with "the" in front
        better_version.append("the " + org.lower())
        better_version.append("the " + org.title())

    # write to file
    save_data_json(
        "extracted_fields/data/mrb_organizations.json", better_version)

    return (better_version)


def create_training_data(file, type):
    data = load_data_json(file)

    patterns = []
    for item in data:
        pattern = {
            "label": type,
            "pattern": item
        }
        patterns.append(pattern)
    return (patterns)


def generate_rules(patterns):
    nlp = English()
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)
    nlp.to_disk("extracted_fields/mrb_refno_ner")


# better_version = generate_better_organization_patterns(
#     "extracted_fields/data/organizations/mrb_organizations.json")


patterns = create_training_data(
    "extracted_fields/data/ref_no/mrb_ref_nums.json", "REF_NO")

save_data_json(
    "extracted_fields/data/ref_no/mrb_ref_nums_patterns.json", patterns)
generate_rules(patterns)
