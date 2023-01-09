import requests
import json

url = "https://gstq.com/products.json?limit=250&page=1"

r = requests.get(url)

data = r.json()
product_list = []

with open('gstqdata2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)