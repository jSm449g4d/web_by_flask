# coding: utf-8
import sys
import os
import flask
from flask import  render_template,redirect,request,render_template_string
from werkzeug.utils import secure_filename
import importlib
import zipfile
import threading
import random
from datetime import datetime
import pytz
import time
from sqlalchemy import create_engine
import json
from google.cloud import storage
import firebase_admin
from firebase_admin import auth


def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

#Flask_Startup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join("./",os.path.dirname(__file__)))
app = flask.Flask(__name__)
#prevent uploading too large file
app.config['MAX_CONTENT_LENGTH'] = 100000000
#management of status_table
status_table=""
def add_status_table(title="",data="",color="navy"):
    global status_table
    status_table+="<tr><td style=\"color:"+color+";\">"+title+"</td><td style=\"color:"+color+";\">"+data+"</td></tr>"
add_status_table("Python",sys.version,color="#555000")
add_status_table("Flask",flask.__version__,color="#555000")
access_counter=0
#unzip CDN contents for fallback
try:zipfile.ZipFile(os.path.join("./static/","bootstrap-4.4.1-dist.zip")).extractall("./static/")
except:print("cant unzip CDN contents")

#management of ORMapper
try:
    with open("MySQL_key.json","r") as fp:
        MySQL_key=json.load(fp)
        dbengine = create_engine("mysql+mysqldb://"+MySQL_key["user"]+":"+MySQL_key["password"]+
                                "@"+MySQL_key["host"]+"/"+MySQL_key["db"]+"?charset=utf8",encoding = "utf-8")
        add_status_table("DB","MySQL")
        storage_client = storage.Client.from_service_account_json("FirebaseAdmin_Key.json")
        cred = firebase_admin.credentials.Certificate("FirebaseAdmin_Key.json")
        firebase_admin.initialize_app(cred)
        add_status_table("GCP","available:%Y/%m/%d %H:%M:%S (UTC)")
except:
    dbengine = create_engine('sqlite:///flask.sqlite3',encoding = "utf-8")
    #os.chmod("./flask.sqlite3",0o777)
    add_status_table("DB","sqlite3")


@app.route("/")
def indexpage_show():
    global access_counter;access_counter+=1
    return render_template_2("index.html",
    STATUS_TABLE=status_table,
    access_counter=str(access_counter)
    )

@app.route("/<name>.html")
def html_show(name):
    try :return render_template('./'+name+'.html')
    except:return redirect('./'),404

@app.route("/<name>.py",methods=['GET', 'POST'])
def py_show(name):
    try :return importlib.import_module(name).show(request)
    except Exception as e:
        return render_template("error.html",
        form_error_code="500",form_error_text=str(e)),500

application=app

if __name__ == "__main__":
    app.run()
