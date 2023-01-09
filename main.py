import requests
import pandas as pd
import json
import requests
import grab_token as grab
from io import StringIO
from html.parser import HTMLParser
import csv
import os

url = "https://gstq.com/products.json?limit=250&page=1"

r = requests.get(url)

data = r.json()
product_list = []



# class html Parser for description of products
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

# assign html parser class to variable and feed data into parser
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# Pull style data and dump data into json file -> return style data
def get_styleData():
    style_request = requests.get(url)
    style_data = style_request.json()
    with open(os.path.join('G:\DEVL\webscrape_joor\misc','data.json'), 'w', encoding='utf-8') as f:
        json.dump(style_data, f, ensure_ascii=False, indent=4)
    return style_data

# Organize the style data that was pulled
def organize_styleData():
    style_data = get_styleData()

    for item in data["products"]:
        title = item['title']
        handle = item['handle']
        created = item['created_at']
        description = item['body_html']
        product_type = item['product_type']
        product_id = item['id']

        for image in item['images']:
            try:
                imagesrc = image['src']
            except:
                imagesrc = 'None'

        for option in item['options']:

            option_name = option['name']
            option_values = option['values']

        for variant in item['variants']:
            price = variant['price']
            sku = variant['sku']
            available = variant['available']
            size_name = variant['option2']

        # Check if option is Color or Size
        if option_name == 'Color':
            color_option = option_values
        elif option_name != 'Color':
            color_option = "null"

        if option_name == 'Size':
            size_name = option_values
        else:
            pass
  
        # Add prices, colors, and sizes into their own dictionary
        # this structures the data to the bulk endpoint
        # Style price
        price = {
            'price_label': 'USD',
            'price_currency': 'USD',
            'price_wholesale': price
        }
        # Style color
        color = {
            'color_name': color_option,
            'color_code': color_option,
        }

        # Style size
        size = {
            'size_name': size_name,
        }      

        # Add all values into another dictionary and add peripheral dictionaries from above
        # this will put the above dictionaries into a list
        style = {
            'style_name': title,
            'silhouette': product_type,
            'sku': sku,
            'available': available,
            'image': imagesrc,
            'option': option_name,
            'prices': [price],
            'colors': [color],
            'sizes': [size]
        }

        # Create a dictionary and assign it to the style key
        style_dict = {
            "style": [style],
        }
    
        bulkstyle_dict = {
            "bulk_style": style_dict
        }

        product_list.append(style_dict)
    for x in product_list:
        bulkstyle_dict = {
            "bulk_style": product_list
    }


    return bulkstyle_dict

# Dump organized data into json file
with open(os.path.join('G:\DEVL\webscrape_joor\misc','clean_productdata.json'), 'w', encoding='utf-8') as f:
    json.dump(organize_styleData(), f, ensure_ascii=False, indent=4)


# joor base url
base_url = "https://apisandbox.jooraccess.com/v2/"
url = "style-number/?count=100"

# joor class to initialize header
class JOOR:
    API_TOKEN = grab.token
    def __init__(self):
        self.header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.API_TOKEN}"
        }

    def get_header(self):
        header = self.header
        return header

global_API_TOKEN = grab.token
header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "authorization": f"Bearer {global_API_TOKEN}"
}


req = requests.get(base_url+url, header)

#print(req_class)
print("\n\n")
print(req)
print("\n\n")
print(req.content)
print("\n\n")
print(req.headers)
print("\n\n")
print(req.request)




