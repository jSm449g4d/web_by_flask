from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os 
from janome.tokenizer import Tokenizer
import gc
import zipfile

DataDir="./ymm3toymm4/"

def ffzk(input_dir):#Relative directory for all existing files
    imgname_array=[];input_dir=input_dir.strip("\"\'")
    for fd_path, _, sb_file in os.walk(input_dir):
        for fil in sb_file:imgname_array.append(fd_path.replace('\\','/') + '/' + fil)
    if os.path.isfile(input_dir):imgname_array.append(input_dir.replace('\\','/'))
    return imgname_array

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def show(req):
    os.chdir(os.path.dirname(__file__))
    if not os.path.exists(DataDir):os.mkdir(DataDir)
    if req.method == 'POST':
        if 'submit_1' in req.form and secure_filename(req.form['submit_1'])=="True":
            for material in req.files.getlist('upload_1'):
                target=material.filename.translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
                print(material)
                material.save(os.path.join(DataDir,target))

        if 'submit_2' in req.form and secure_filename(req.form['submit_2'])=="True":
            if 'upload_2' in req.files:
                target=req.files['upload_2'].filename.translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
                req.files['upload_2'].save(os.path.join(DataDir,target))
                with zipfile.ZipFile(os.path.join(DataDir,target)) as z:
                    z.extractall(DataDir)


    return render_template_2("ymm3toymm4.html")
