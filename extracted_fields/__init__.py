import spacy
from spacy.lang.en import English

# with open("/Users/nitieii/Desktop/DLM-MLT-00001-22-E&V.txt", "r") as f:
#     text = f.read()

text = 'HANOI PEOPLES COMMITTEE HANOI METROPOLITAN RAILWAY MANAGEMENT BOARD No: 226/QD-DSDT-KTTD SOCIALIST REPUBLIC OF VIETNAM Independence - Freedom - Happiness Hanoi, December 24 2018 DECISION On the approval of the construction drawing design (CDD) of the item: U frame and Trench at Ramp -CP03: Tunnel and underground stations under Hanoi Pilot Light Metro Line project, section Nhon - Hanoi Station GENERAL DIRECTOR OF HANOI METROPOLITAN RAILWAY MANAGEMENT BOARD (MRB) Pursuant to: Law on Construction No. 50/2014/QH13;'

nlp_ref = spacy.load("extracted_fields/mrb_refnos_ner_model")
nlp_org = spacy.load("extracted_fields/mrb_organizations_ner_model")

# nlp = spacy.load("en_core_web_sm")
doc_ref = nlp_ref(text)
doc_org = nlp_org(text)

for ent in doc_ref.ents:
    print(ent.text, ent.label_)

for ent in doc_org.ents:
    print(ent.text, ent.label_)
