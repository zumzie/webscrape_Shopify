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
            size_list = []
            price = variant['price']
            sku = str(variant['sku'])
            upc = str(variant['id'])
            prod_id = str(variant['product_id'])
            available = variant['available']
            #size_name = variant['option2']
            if item['options'][0]['name'] == 'Color' and item['options'][0]['position'] == 1:
                color_name = variant['option1']
            else:
                color_name = None
            if item['options'][0]['name'] == 'Size' and item['options'][0]['position'] == 2:
                size_name = variant['option2']
            else:
                size_name = None
                

        # Check if option is Color or Size
        if option_name == 'Color':
            color_option = option_values
        elif option_name != 'Color':
            color_option = None

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
            'price_wholesale': price,
            'price_retail': price
        }
        # Style color
        color = {
            'color_name': color_name,
            'color_code': color_name,
        }

        # Style size
 
        if size_name is not None and len(size_name)>0:     
            for sizes in size_name:
                try:
                    size_list.append({"size_name": sizes})
                except:
                    size_list.append({"size_name": None})

        try:
            upcs = {
                    'upc': color_name[:3] + str(upc)
                }
        except:
            upcs = {
                'upc': color_name
            }

        style = {
            'style_name': title,
            'style_number': str(sku) or str(upc),
            'style_identifier': str(prod_id) or str(upc),
            'style_description': description,
            'silhouette': product_type,
            'available': available,
            'image': imagesrc,
            'prices': [price],
            'colors': [color],
            'sizes': size_list,          
        }


        # Create a dictionary and assign it to the style key
        style_dict = {
            "style": [style],
        }

        product_list.append(style)
    
    bulkstyle_dict = {
        "bulk_styles": {
            "style": product_list
        }
    }

    return bulkstyle_dict

# Dump organized data into json file
with open(os.path.join('G:\DEVL\webscrape_joor\misc','clean_productdata.json'), 'w', encoding='utf-8') as f:
    json.dump(organize_styleData(), f, ensure_ascii=False, indent=2)


# joor base url
base_url = "https://apisandbox.jooraccess.com/v2/style-number/?count=100"
bulk_url = "https://apisandbox.jooraccess.com/v2/bulk-style"
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


req = requests.get(base_url, header)


#print(req_class)
print("\n\n")
print(req)
print("\n\n")
print(req.content)
print("\n\n")
print(req.headers)
print("\n\n")
print(req.request)



response = requests.post(bulk_url, organize_styleData(), headers=header)
#print(req_class)
print("\n\n")
print(response)
print("\n\n")
print(response.content)
print("\n\n")
print(response.headers)
print("\n\n")
print(response.request)



