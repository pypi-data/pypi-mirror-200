__author__="Ayush Yajnik"

import requests
import warnings
import sys

sys.path.append("..")

class cyberark:

    def __init__(self,data):
        self.data = data
        self.appId = self.data['appId']
        self.safe = self.data['safe']
        self.object = self.data['object']
        self.hostname = self.data['hostname']
        self.username = self.data['username']
        self.base_url = "https://"+self.hostname+"/AIMWebService/api/Accounts?"

        if self.object != None:
            self.full_path_1 = self.base_url+"AppID="+self.appId+"&Query=Safe="+self.safe+";Object="+self.object
        if self.username != None:
             self.full_path_1 = self.base_url+"AppID="+self.appId+"&Query=Safe="+self.safe+"&Username="+self.username
        if self.object != None and self.username != None:
             self.full_path_1 = self.base_url+"AppID="+self.appId+"&Query=Safe="+self.safe+";Object="+self.object+"&Username="+self.username

    def getPasswordFromCyberArk(self):
        return self.execute_request()
    
    def execute_request(self):
        if self.object != None:
            self.full_path_1 = self.base_url+"AppID="+self.appId+"&Query=Safe="+self.safe+";Object="+self.object
        if self.username != None:
             self.full_path_1 = self.base_url+"AppID="+self.appId+"&Query=Safe="+self.safe+"&Username="+self.username
        if self.object != None and self.username != None:
             self.full_path_1 = self.base_url+"AppID="+self.appId+"&Query=Safe="+self.safe+";Object="+self.object+"&Username="+self.username


        payload = ''
        headers = {}
        if self.full_path_1[0:8] == "https://":
            path1 = self.full_path_1
        else:
            path1 = "https://"+self.full_path_1

        warnings.filterwarnings('ignore',message = "Unverified HTTPS request")

        try:
            requesting = requests.get(path1,data=payload,headers=headers,verify=False,timeout=30)
        except requests.ConnectionError as e:
            sys.exit(str(e)+"\nCyberArk connection Error when trying to get password from below link\n"+path1)
        except requests.Timeout as e:
            sys.exit(str(e)+"\nConnection establishment to the link timed out\n"+path1)
        except requests.RequestException as e:
            sys.exit(str(e)+"\nCyberArk Connection General Error when trying to get password from the below link\n"+path1)
        except KeyboardInterrupt:
            sys.exit("Someone closed the program abruptly")

        return requesting.json()

