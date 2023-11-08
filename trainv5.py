import random
import json
from tqdm import tqdm
import spacy
from spacy.training import Example

JSON_FILE = 'annotations.json'

def create_annotations(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        entity_name = 'PRODUCT'
        train_data = data['annotations']
        train_data = [x for x in train_data if x is not None]

        for i in train_data:
            if i[1]['entities'] == []:
                i[1]['entities'] = (0, 0, entity_name),
            else:
                i[1]['entities'][0] = tuple(i[1]['entities'][0])
        return train_data

def train_model(train_data):
    nlp = spacy.blank('en')
    if 'ner' not in nlp.pipe_names:
        ner = nlp.add_pipe('ner', last=True)

    for _, annotations in train_data:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(100):
            random.shuffle(train_data)
            losses = {}
            for text, annotations in tqdm(train_data):
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], drop=0.5, losses=losses)
            print(losses)

    nlp.to_disk('./v5_product_ner_model')


if __name__ == '__main__':
    TRAIN_DATA = create_annotations(JSON_FILE)
    print(TRAIN_DATA)
    train_model(TRAIN_DATA)
