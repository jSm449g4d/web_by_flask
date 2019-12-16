# coding: utf-8
import sys
import os
import flask
from flask import  render_template,redirect,request
import importlib
import sqlite3
import zipfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join("./",os.path.dirname(__file__)))

app = flask.Flask(__name__)

#prevent uploading too large file
app.config['MAX_CONTENT_LENGTH'] = 100000000

#unzip CDN contents for fallback
try:zipfile.ZipFile(os.path.join("./static/","bootstrap-4.4.1-dist.zip")).extractall("./static/")
except:print("cant unzip CDN contents")

@app.route("/")
def indexpage_show():
   return render_template("index.html",
   used_python=sys.version,
   used_flask=flask.__version__,
   used_sqlite3=sqlite3.version)

@app.route("/<name>.html")
def html_show(name):
    try :return render_template('./'+name+'.html')
    except:return redirect('./')

@app.route("/<name>.py",methods=['GET', 'POST'])
def py_show(name):
    try :return importlib.import_module(name).show(request)
    except:return redirect('./')

application=app

if __name__ == "__main__":
    app.run()
