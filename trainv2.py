import csv
import spacy
from spacy.training.example import Example
import random

nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")
ner.add_label("PRODUCT")

training_data = []
with open('shop_scraper/products_without_labels.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        training_data.append(
            (str(row[0]), {"entities": [(0, row[0].__len__(), 'PRODUCT')]}))

n_iter = 10
print(n_iter)
optimizer = nlp.begin_training()
for itn in range(n_iter):
    random.shuffle(training_data)
    losses = {}
    for text, annotations in training_data:
        print(text)
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], drop=0.5, losses=losses)
    print(losses)

nlp.to_disk("v2_product_ner_model")
