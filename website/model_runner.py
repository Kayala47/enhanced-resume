import spacy
import sys


# grab the directory where the model is stored
model_dir = "../ner/spacy_model"

def run_ner_model(data):
    nlp2 = spacy.load(model_dir)
    finalData = []
    for value in data:
        doc = nlp2(value)
        finalData.append([(ent.text, ent.label_) for ent in doc.ents])
        # print("Tagged item " + str(index) + " out of " + str(len(data)))

    return finalData

if __name__ == "__main__":
    print(run_ner_model([sys.argv[1]]))
    