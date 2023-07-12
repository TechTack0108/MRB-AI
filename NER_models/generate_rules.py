from file_utils import load_data_json, save_data_json
from spacy.lang.en import English


def generate_better_organization_patterns(file):
    data = load_data_json(file)

    better_version = data

    # append lowercase, camelcase of each organization
    for org in list(data):
        better_version.append(org.lower())
        better_version.append(org.title())

        # append lowercase, camelcase of each organization with "the" in front
        better_version.append("the " + org.lower())
        better_version.append("the " + org.title())

        # append "(" and ") for each organization
        better_version.append("(" + org + ")")

    # write to file
    save_data_json(
        "../data/trained_data/organizations/mrb_better_organizations.json", better_version)

    return better_version


def create_training_data(file, type):
    data = load_data_json(file)

    patterns = []
    for item in data:
        pattern = {
            "label": type,
            "pattern": item
        }
        patterns.append(pattern)
    return patterns


def generate_rules(patterns_data):
    nlp = English()
    ruler = nlp.add_pipe("entity_ruler")
    # noinspection PyUnresolvedReferences
    ruler.add_patterns(patterns_data)
    nlp.to_disk("mrb_organizations_ner")


better_version = generate_better_organization_patterns(
    "../data/trained_data/organizations/mrb_organizations.json")

patterns = create_training_data(
    "../data/trained_data/organizations/mrb_better_organizations.json", "ORG")

save_data_json("../data/trained_data/organizations/mrb_organizations_patterns.json", patterns)

# patterns = create_training_data(
#     "../data/trained_data/ref_no/mrb_ref_nums.json", "REF_NO")
#
# save_data_json("../data/trained_data/ref_no/mrb_ref_nums_patterns.json", patterns)

# patterns = create_training_data(
#     "../data/trained_data/date/mrb_dates.json", "DATE")
#
# save_data_json(
#     "../data/trained_data/date/mrb_dates_patterns.json", patterns)

generate_rules(patterns)
