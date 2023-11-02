import spacy
from spacy.training.example import Example
import random
import requests
from bs4 import BeautifulSoup
import json


def extract_categories(url, unique_list):
    try:
        additional_training_data = []
        no_of_products = 0
        for index, u_category in enumerate(unique_list):
            cat_res = requests.get(
                url + u_category['uri'])
            if cat_res.status_code == 200:
                html_content = cat_res.text
                soup = BeautifulSoup(html_content, 'html.parser')
                product_elements = soup.find_all(
                    'h3', class_="card__heading")
                for product in product_elements:
                    product_name_raw = product.find('a').text
                    product_name = product_name_raw.strip()
                    try:
                        start_index_in_page = product_name_raw.index(
                            product_name)
                    except ValueError:
                        continue
                    end_index_in_page = start_index_in_page + \
                        len(product_name)
                    additional_training_data.append(
                        (product_name_raw, {"entities": [(start_index_in_page, end_index_in_page, "PRODUCT")]}))
                page = 2
                while len(product_elements):
                    cat_res_new_page = requests.get(
                        url + u_category['uri']+"?page="+str(page))
                    if cat_res_new_page.status_code == 200:
                        html_content = cat_res_new_page.text
                        soup = BeautifulSoup(
                            html_content, 'html.parser')
                        product_elements = soup.find_all(
                            'h3', class_="card__heading")
                        for product in product_elements:
                            product_name_raw = product.find('a').text
                            product_name = product_name_raw.strip()
                            try:
                                start_index_in_page = product_name_raw.index(
                                    product_name)
                            except ValueError:
                                continue
                            end_index_in_page = start_index_in_page + \
                                len(product_name)
                            additional_training_data.append(
                                (product_name_raw, {"entities": [(start_index_in_page, end_index_in_page, "PRODUCT")]}))
                        print('page:', page, 'in', u_category['name'])
                    else:
                        break
                    page += 1
                print(index)

            else:
                print(index)
        print(no_of_products, 'products found.', )
        return additional_training_data

    except Exception as err:
        print(err)


url = 'https://www.factorybuys.com.au'
if __name__ == "__main__":
    with open('categories.json', 'r') as json_file:
        unique_list = json.load(json_file)
        training_data = extract_categories(url, unique_list=unique_list)
        nlp = spacy.load("custom_ner_model")
        random.shuffle(training_data)
        losses = {}
        for text, annotations in training_data:
            example = Example.from_dict(
                nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.5, losses=losses)
            print(losses)
        nlp.to_disk("custom_ner_model")
