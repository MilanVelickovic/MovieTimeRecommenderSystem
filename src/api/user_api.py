import requests
from dotenv import load_dotenv
import os

load_dotenv()

class UserAPI:
    def __init__(self) -> None:
        self.base_url: str = "http://localhost:9000/user/"
        self.security_code: str = os.getenv("USER_API_SEC_CODE")
    
    def getAllUsers(self) -> dict:
        data = {
            "securityCode": self.security_code
        }

        return requests.get(self.base_url + "all", data= data).json()