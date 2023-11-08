import spacy
from spacy.training.example import Example
import random
import requests
from bs4 import BeautifulSoup
import json


def save_annotation(description):
    with open('product_description_v5.txt', 'a', encoding='utf-8') as f:
        f.write(
            f"{description}\n")


def extract_categories(url, unique_list):
    try:
        for index, u_category in enumerate(unique_list[47:]):
            print(
                f'Working on url {index} of {len(unique_list[47:])}. - {u_category["uri"]}')
            cat_res = requests.get(
                url + u_category['uri'])
            if cat_res.status_code == 200:
                html_content = cat_res.text
                soup = BeautifulSoup(html_content, 'html.parser')
                product_elements = soup.find_all(
                    'h3', class_="card__heading")
                for product in product_elements:
                    product_tag = product.find('a', href=True)
                    product_link = product_tag['href']
                    prod_res = requests.get(url + product_link)
                    if prod_res.status_code == 200:
                        html_content = prod_res.text
                        soup = BeautifulSoup(html_content, 'html.parser')
                        description_tag = soup.find(
                            'div', class_='description-custom-content')
                        if description_tag:
                            description = description_tag.get_text(strip=True)
                            if description:
                                save_annotation(description)

    except Exception as err:
        print(err)


url = 'https://www.factorybuys.com.au'
if __name__ == "__main__":
    with open('categories.json', 'r') as json_file:
        unique_list = json.load(json_file)
        extract_categories(url, unique_list=unique_list)
