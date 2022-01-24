import requests

class UserAPI:
    def __init__(self):
        self.base_url = "http://localhost:9000/user/"
        self.security_code = "7=_%=g@n<^[EBfM^"
    
    def getAllUsers(self):
        return requests.get(self.base_url + "all", data= {"securityCode": self.security_code}).json()