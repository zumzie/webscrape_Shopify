

class Images:
    def __init__(self):
        self.base_url = "https://apisandbox.jooraccess.com/v2/"
        self.bulkurl = ""

    def bulk_endpoint(self):
        bulk_url = self.base_url + self.bulkurl
        return bulk_url
