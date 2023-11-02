import spacy
from spacy.training.example import Example
import random

# Load the base spaCy model (e.g., 'en_core_web_sm')
nlp = spacy.load("en_core_web_sm")

# Create a new NER component if not already available
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Define labels (e.g., "PRODUCT")
labels = ["PRODUCT"]

# Add labels to the NER component
for label in labels:
    ner.add_label(label)

# Create training examples from labeled data
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

# Training the NER model
n_iter = 10
for _ in range(n_iter):
    random.shuffle(training_data)  # Optional: Shuffle the training data
    losses = {}
    for text, annotations in training_data:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], drop=0.5, losses=losses)

# Save the trained model
nlp.to_disk("furniture_product_ner")

# Load the trained model
furniture_ner = spacy.load("furniture_product_ner")

# Inference using the trained model
text = "A beautiful OLED TV is available in our store."
doc = furniture_ner(text)
for ent in doc.ents:
    print(ent.text, ent.label_)
