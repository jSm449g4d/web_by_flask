from flask import  render_template_string,send_file,render_template
from werkzeug.utils import secure_filename
import os 
import sqlite3
import hashlib
import datetime

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def show(req):
    os.chdir(os.path.dirname(__file__))
    if req.method == 'POST':
        0
    return render_template("bootstraptest.html")
