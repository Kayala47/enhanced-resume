import spacy
import sys


# grab the directory where the model is stored
model_dir = "./output/ner"

def run_ner_model(data):
    nlp2 = spacy.load(model_dir)
    finalData = []
    for item in data:
        doc = nlp2(item)
        finalData.append([(ent.text, ent.label_) for ent in doc.ents])

    return finalData

if __name__ == "__main__":
    print(run_ner_model([sys.argv[1]]))
    