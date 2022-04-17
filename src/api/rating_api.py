import requests
from dotenv import load_dotenv
import os

load_dotenv()

class RatingAPI:
    def __init__(self):
        self.base_url: str = "http://localhost:9000/rate/"
        self.security_code: str = os.getenv("RATING_API_SEC_CODE")
    
    def getAllRatings(self):
        data = {
            "securityCode": self.security_code
        }
        
        return requests.get(self.base_url + "all", data= data).json()