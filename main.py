import requests
import json
import csv

url = "https://stickandball.com/products.json?limit=250&page=1"

r = requests.get(url)

data = r.json()
product_list = []

for item in data['products']:
    title = item['title']
    handle = item['handle']
    created = item['created_at']
    product_type = item['product_type']

    for image in item['images']:
        try:
            imagesrc = image['src']
        except:
            imagesrc = 'None'
    for variant in item['variants']:
        price = variant['price']
        sku = variant['sku']
        available = variant['available']

        product = {
            'title': title,
            'handle': handle,
            'created': created,
            'product_type': product_type,
            'price': price,
            'sku': sku,
            'available': available,
            'image': imagesrc
        }
        
        product_list.append(product)
    
print(product_list)



