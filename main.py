import requests
import pandas as pd
import json
import requests
import grab_token as grab
from requests import Session
import csv

url = "https://gstq.com/products.json?limit=250&page=1"

r = requests.get(url)

data = r.json()
product_list = []

for item in data['products']:
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
        
        product_list.append(product)
    
df = pd.DataFrame(product_list)

df.to_csv('testrun2.csv')
print('test)')



url = "https://apisandbox.jooraccess.com/v2/style-number/?count=100"

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

req_class = requests.get(url, headers=JOOR.get_header)
req = requests.get(url, headers=header)

print(req_class)
print("\n\n")
print(req)





