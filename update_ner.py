import spacy
from spacy.training.example import Example
import random
import requests
from bs4 import BeautifulSoup
import re
import json


def extract_categories(url, uri):
    try:
        res = requests.get(url + uri)
        if res.status_code == 200:
            html_content = res.text
            soup = BeautifulSoup(html_content, 'html.parser')
            category_elements = soup.find_all('h3', class_="card__heading")
            categories = []
            for category in category_elements:
                category_name = category.find('a').text.strip()
                category_uri = category.find('a', href=True)['href'].strip()
                if '/collections/all' not in category_uri:
                    categories.append({
                        'name': category_name,
                        'uri': category_uri
                    })

            unique_list = [dict(t)
                           for t in {tuple(d.items()) for d in categories}]
            products_by_category = []
            no_of_products = 0
            print(unique_list)
            # with open('categories.json', 'w') as json_file:
            #     json.dump(unique_list, json_file)
            # for u_category in unique_list:
            #     cat_res = requests.get(
            #         url + u_category['uri'])
            #     if cat_res.status_code == 200:
            #         html_content = cat_res.text
            #         soup = BeautifulSoup(html_content, 'html.parser')
            #         product_elements = soup.find_all(
            #             'h3', class_="card__heading")
            #         products = []
            #         for product in product_elements:
            #             product_name_raw = product.find('a').text
            #             product_name = product_name_raw.strip()
            #             try:
            #                 start_index_in_page = html_content.index(
            #                     product_name_raw)
            #             except ValueError:
            #                 continue
            #             end_index_in_page = start_index_in_page + \
            #                 len(product_name_raw)
            #             products.append(
            #                 [start_index_in_page, end_index_in_page, product_name])
            #         page = 2
            #         while len(product_elements):
            #             cat_res_new_page = requests.get(
            #                 url + u_category['uri']+"?page="+str(page))
            #             if cat_res_new_page.status_code == 200:
            #                 html_content = cat_res_new_page.text
            #                 soup = BeautifulSoup(
            #                     html_content, 'html.parser')
            #                 product_elements = soup.find_all(
            #                     'h3', class_="card__heading")
            #                 for product in product_elements:
            #                     product_name_raw = product.find('a').text
            #                     product_name = product_name_raw.strip()
            #                     try:
            #                         start_index_in_page = html_content.index(
            #                             product_name_raw)
            #                     except ValueError:
            #                         continue
            #                     end_index_in_page = start_index_in_page + \
            #                         len(product_name_raw)
            #                     products.extend(
            #                         [start_index_in_page, end_index_in_page, product_name])
            #             else:
            #                 break
            #             page += 1

            #         products_by_category.append({
            #             'category': u_category['name'],
            #             'uri': u_category['uri'],
            #             'products': products
            #         })
            #         print(products_by_category)
            #         no_of_products += len(products)
            #     print(no_of_products, 'products found.', )
    except Exception as err:
        print(err)


url = 'https://www.factorybuys.com.au'
if __name__ == "__main__":
    extract_categories(url, uri='/products')
# nlp = spacy.load("custom_ner_model")

# additional_data = [
#     ("Our modern dining table is a top seller.", "dining table"),
#     ("Discover the elegant glass chandelier.", "glass chandelier"),

# ]


# additional_training_data = []
# for text, product_name in additional_data:
#     start = text.index(product_name)
#     end = start + len(product_name)
#     additional_training_data.append(
#         (text, {"entities": [(start, end, "PRODUCT")]}))

# training_data = additional_training_data

# n_iter = 10

# for _ in range(n_iter):
#     random.shuffle(training_data)
#     losses = {}
#     for text, annotations in training_data:
#         example = Example.from_dict(nlp.make_doc(text), annotations)
#         nlp.update([example], drop=0.5, losses=losses)
#     print(losses)

# nlp.to_disk("custom_ner_model")
