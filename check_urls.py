import pandas as pd
import requests
from fake_useragent import UserAgent
import time


def is_url_accessible(url):
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False


def process_csv(input_csv, output_xlsx):
    data = pd.read_csv(input_csv, header=None, names=['URL'])
    is_accessible = []

    for url in data['URL']:
        if is_url_accessible(url):
            is_accessible.append(True)
        else:
            is_accessible.append(False)

    data['IsAccessible'] = is_accessible
    data.to_excel(output_xlsx, index=False)


if __name__ == "__main__":
    input_csv_file = "furniture_stores_pages.csv"
    output_xlsx_file = "result_without_async.xlsx"

    process_csv(input_csv_file, output_xlsx_file)

    print(f"Results saved to {output_xlsx_file}")
