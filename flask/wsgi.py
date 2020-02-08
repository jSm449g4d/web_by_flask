# coding: utf-8
import sys
import os
import flask
from flask import  redirect,request,render_template_string,render_template
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

#Flask_Startup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join("./",os.path.dirname(__file__)))
app = flask.Flask(__name__)
wsgi_util=importlib.import_module("wsgi_util")
#prevent uploading too large file
app.config['MAX_CONTENT_LENGTH'] = 100000000
#unzip CDN contents for fallback
try:zipfile.ZipFile(os.path.join("./static/","bootstrap-4.4.1-dist.zip")).extractall("./static/")
except:print("cant unzip CDN contents")
wsgi_util.Resource_Reload()

@app.route("/")
def indexpage_show():
    wsgi_util.access_counter+=1
    return wsgi_util.render_template_2("index.html",
    STATUS_TABLE=wsgi_util.status_table,
    access_counter=str(wsgi_util.access_counter)
    )

@app.route("/<name>.html")
def html_show(name):
    try :return wsgi_util.render_template_2('./'+name+'.html')
    except:return redirect('./'),404

@app.route("/<name>.py",methods=['GET', 'POST'])
def py_show(name):
    try :return importlib.import_module(name).show(request)
    except Exception as e:
        return wsgi_util.render_template_2("error.html",
        form_error_code="500",form_error_text=str(e)),500

application=app

if __name__ == "__main__":
    app.run()
