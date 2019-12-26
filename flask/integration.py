#Integration test 2/2

# coding: utf-8
import sys
import urllib.parse
from bs4 import BeautifulSoup
import requests
import time

if __name__ == "__main__":    
    html="";connect_try_count=0
    while True:#If the server still doesn't start
        try :html=requests.get("http://127.0.0.1:8080/").text;break
        except:time.sleep(1);connect_try_count+=1
        if 3<connect_try_count:
            raise Exception("Error:connection to http://127.0.0.1:8080/")
    
    html=requests.get("http://127.0.0.1:8080/").text
    soup = BeautifulSoup(html,"html.parser")
    element_a=soup.find_all("a")
    for ea in element_a:
        if "./" not in ea["href"]:continue
        #wsgi.py triggers redirect on error
        r = requests.get(urllib.parse.urljoin("http://127.0.0.1:8080/",ea["href"]))
        if r.url!=urllib.parse.urljoin("http://127.0.0.1:8080/",ea["href"]):
            raise Exception("Error_URL:"+urllib.parse.urljoin("http://127.0.0.1:8080/",ea["href"]))
    sys.exit(0)
