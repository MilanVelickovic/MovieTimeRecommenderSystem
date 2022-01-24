import requests

class RatingAPI:
    def __init__(self):
        self.base_url = "http://localhost:9000/rate/"
        self.security_code = "w@>*5ZA{Qe/eH`9P"
    
    def getAllRatings(self):
        return requests.get(self.base_url + "all", data= {"securityCode": self.security_code}).json()