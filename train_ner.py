import spacy
from spacy.training.example import Example
import random

nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")
ner.add_label("PRODUCT-CATEGORY")
ner.add_label("PRODUCT")


training_data = []
labeled_data = [
    ("Check out our new leather sofa.", "leather sofa"),
    ("This wooden coffee table is on sale.", "wooden coffee table"),
    ("Introducing the comfortable recliner chair.", "recliner chair"),
]

for text, product_name in labeled_data:
    start = text.index(product_name)
    end = start + len(product_name)
    training_data.append((text, {"entities": [(start, end, "PRODUCT")]}))

n_iter = 10
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.select_pipes(disable=other_pipes):
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(training_data)
        losses = {}
        for text, annotations in training_data:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(losses)

nlp.to_disk("test_ner_model")
