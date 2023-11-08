import json
import spacy
from spacy.training.example import Example
import random

nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")
ner.add_label("PRODUCT")

training_data = []
with open('products.json', 'r') as json_file:
    categories = json.load(json_file)
    for products_by_category in categories:
        for product_details in products_by_category['products']:
            if type(product_details) == list:
                product = product_details[2]
                training_data.append(
                    (str(product), {"entities": [(0, product.__len__(), 'PRODUCT')]}))


n_iter = 10
optimizer = nlp.begin_training()
for itn in range(n_iter):
    random.shuffle(training_data)
    losses = {}
    for text, annotations in training_data:
        print(text)
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], drop=0.5, losses=losses)
    print(losses)

nlp.to_disk("v3_product_ner_model")
