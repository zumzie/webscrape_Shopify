
class Style:
    def __init__(self):
        self.base_url = "https://apisandbox.jooraccess.com/v2/"
        self.bulkurl = "style-number/?count=100"

    def create_bulkstyles(self):
        bulk_url = self.base_url + self.bulkurl
        return bulk_url

    def create_style(self):
        bulk_url = self.base_url + self.bulkurl
        return bulk_url
    
    def get_stylesByCount(self):
        bulk_url = self.base_url + self.bulkurl
        return bulk_url

    def get_styleByID(self):
        bulk_url = self.base_url + self.bulkurl
        return bulk_url