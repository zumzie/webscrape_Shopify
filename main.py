import requests
import pandas as pd
import json
import requests
import grab_token as grab
from io import StringIO
from html.parser import HTMLParser
import csv

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
    with open('data.json', 'w', encoding='utf-8') as f:
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
            color_option = variant['option2']

        product = {
            'title': title,
            'handle': handle,
            'created': created,
            'product_type': product_type,
            'price': price,
            'sku': sku,
            'available': available,
            'image': imagesrc,
            'option': option_name,
            'option_values': option_values,
            'option2': color_option   
        }

        style_dict = {
            "style": [product]
        }
            
        product_list.append(style_dict)
        for style in style_dict:
            bulkstyle_dict = {
                "bulk_styles": product_list
            }
    return bulkstyle_dict

print(organize_styleData())

# Dump organized data into json file
with open('clean_productdata.json', 'w', encoding='utf-8') as f:
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






req = requests.get(base_url+url, headers=header)

#print(req_class)
print("\n\n")
print(req)
print("\n\n")
print(req.content)
print("\n\n")
print(req.headers)
print("\n\n")
print(req.request)




