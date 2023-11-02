import asyncio
import pandas as pd
import aiohttp
import matplotlib.pyplot as plt
from io import BytesIO
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image


async def is_url_accessible(session, url):
    try:
        async with session.get(url) as response:
            return response.status == 200
    except aiohttp.ClientError:
        return False


async def process_csv(input_csv, output_xlsx):
    async with aiohttp.ClientSession() as session:
        data = pd.read_csv(input_csv, header=None, names=['URL'])
        tasks = []

        for url in data['URL']:
            task = is_url_accessible(session, url)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        data['IsAccessible'] = results

        # Generate the pie chart
        pie_chart = generate_pie_chart(data['IsAccessible'])

        # Create a BytesIO object to save the Excel file
        output = BytesIO()

        # Save the data to a sheet
        data.to_excel(output, sheet_name='Results',
                      index=False, engine='openpyxl')

        # Create a new sheet for the pie chart
        pie_chart.to_excel(output, sheet_name='PieChart',
                           index=False, engine='openpyxl')

        # Save the BytesIO object to a file
        with open(output_xlsx, 'wb') as f:
            f.write(output.getvalue())

        print(f"Results and pie chart saved to {output_xlsx}")


def generate_pie_chart(accessibility_series):
    accessible_count = accessibility_series.value_counts().get(True, 0)
    not_accessible_count = accessibility_series.value_counts().get(False, 0)
    labels = ['Accessible', 'Not Accessible']
    sizes = [accessible_count, not_accessible_count]

    colors = ['#66b3ff', '#ff9999']
    # Create a pie chart using matplotlib
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Accessibility Statistics')
    plt.savefig('pie_chart.png')

    return pd.DataFrame({'Category': labels, 'Count': sizes})


if __name__ == "__main__":
    input_csv_file = "furniture_stores_pages.csv"
    output_xlsx_file = "result_with_pie_chart.xlsx"

    asyncio.run(process_csv(input_csv_file, output_xlsx_file))
