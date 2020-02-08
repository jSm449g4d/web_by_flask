# coding: utf-8
import sys
import os
import flask
from flask import  redirect,request,render_template_string
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

#AP_setting_management
access_counter=0;status_table=""
dbengine = create_engine('sqlite:///flask.sqlite3',encoding = "utf-8")
print(str(dbengine))
def add_status_table(title="",data="",color="navy"):
    global status_table
    status_table+="<tr><td style=\"color:"+color+";\">"+title+"</td><td style=\"color:"+color+";\">"+data+"</td></tr>"
def Resource_Reload():
    global status_table,dbengine;status_table="";dbengine.dispose()
    add_status_table("Python",sys.version,color="#555000")
    add_status_table("Flask",flask.__version__,color="#555000")
    try:
        with open("MySQL_key.json","r") as fp:
            MySQL_key=json.load(fp)
            dbengine = create_engine("mysql+mysqldb://"+MySQL_key["user"]+":"+MySQL_key["password"]+
                                    "@"+MySQL_key["host"]+"/"+MySQL_key["db"]+"?charset=utf8",encoding = "utf-8")
            storage_client = storage.Client.from_service_account_json("FirebaseAdmin_Key.json")
            cred = firebase_admin.credentials.Certificate("FirebaseAdmin_Key.json")
            firebase_admin.initialize_app(cred)
            add_status_table("DB","MySQL",color="#555000")
            add_status_table("GCP",datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)"))
    except:
        dbengine = create_engine('sqlite:///flask2.sqlite3',encoding = "utf-8")
        add_status_table("DB","SQLite3",color="#555000")
        add_status_table("CAUTION","FALLBACK_MODE because cant use online resource",color="red")