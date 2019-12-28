#Integration test 2/2

# coding: utf-8
import sys
import urllib.parse
from bs4 import BeautifulSoup
import requests
import time

if __name__ == "__main__":    
    connect_try_count=0
    while True:#If the server still doesn't start
        try :requests.get("http://127.0.0.1:8080/");break
        except:time.sleep(1);connect_try_count+=1
        if 3<connect_try_count:
            raise Exception("Error:connection to http://127.0.0.1:8080/")
    
    r=requests.get("http://127.0.0.1:8080/")
    if r.status_code!=200:raise Exception("Error_URL:"+"http://127.0.0.1:8080/")
    soup = BeautifulSoup(r.text,"html.parser")
    element_a=soup.find_all("a")
    for ea in element_a:#SPA
        if ea["href"].startswith("./") ==False:continue
        r = requests.get(urllib.parse.urljoin("http://127.0.0.1:8080/",ea["href"]))
        if r.status_code!=200:raise Exception("http://127.0.0.1:8080/",ea["href"])
        
    print("ok")
