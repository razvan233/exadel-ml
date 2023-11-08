import pandas as pd
import json
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin


JSON_FILE = 'annotations.json'
TRAIN_DATA = []


def create_annotations(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

        entity_name = 'PRODUCT'

        train_data = data['annotations']
        train_data = [x for x in train_data if x is not None]
        train_data = [tuple(i) for i in train_data]

        for i in train_data:
            if i[1]['entities'] == []:
                i[1]['entities'] = (0, 0, entity_name)
            else:
                i[1]['entities'][0] = tuple(i[1]['entities'][0])

        return train_data


def train_model(train_data):

    nlp = spacy.blank('en')
    db = DocBin()
    for text, annot in tqdm(train_data):
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot['entities']:
            span = doc.char_span(start, end, label=label,
                                 alignment_mode='contract')
            if span is None:
                print('Skipping entity')
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk('./train.spacy')


if __name__ == '__main__':
    TRAIN_DATA = create_annotations(JSON_FILE)
    print(TRAIN_DATA)
    train_model(TRAIN_DATA)
