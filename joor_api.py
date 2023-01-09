import requests
import grab_token as grab
from requests import Session


class JOOR:
    API_TOKEN = grab.token
    def __init__(self):
        self.header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.API_TOKEN}"
        }
        self.session = requests.Session()
        self.session.headers.update(self.header)

    def get_products(self):
        self.session.get(URLS.get_styles, headers=self.header)






class URLS:
    def __init__(self, response_format="json"):
        self.format = response_format
        
        # Store / base url
        self.base_url = f"https://apisandbox.jooraccess.com/v2/"

        # Styles
        self.modify_style = "style-number"
        self.bulk_style = "bulk-style"
        self.get_styles =  "style?count=100"

    # Style Functions
    def base_url(self):
        return self.base_url

    def create_style(self):
        return self.base_url + self.modify_style
    
    def create_bulkStyle(self):
        return self.base_url + self.bulk_style
    def get_styles(self):
        return self.base_url + self.get_styles

random = []

JOOR.get_products()