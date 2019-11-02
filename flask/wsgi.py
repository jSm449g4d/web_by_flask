# coding: utf-8
import sys
import os
import flask
from flask import  render_template,redirect,request
import importlib

sys.path.append(os.path.dirname(__file__))

app = flask.Flask(__name__)

#prevent uploading too large file
app.config['MAX_CONTENT_LENGTH'] = 100000000

@app.route("/")
def rootpage():
    return redirect('./index')

@app.route("/index")
def index_show():
   return render_template("/index.html",
   used_python="python "+sys.version,
   used_flask="flask "+flask.__version__)

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
