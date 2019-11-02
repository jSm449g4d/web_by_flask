#8th
#Attention! send_file cause directory traversal!
#secure_filename is preventing traversal
#plz check chmod -R 

from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os 

def htmlwalk():
    html=""
    wlks=os.listdir("./fud")
    
    for wlk in wlks:
        html+="<li>"+"<a class=\"file\" href=\"?dl="+wlk+"\">"+wlk+"</a>\t"
        html+="<form method=\"post\" enctype=\"multipart/form-data\" style=\"display:inline;\">"
        html+="<button name=\"delete\" value=\""+wlk+"\">DEL</button></form></li>"
    return html

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def show(req):    
    os.chdir(os.path.dirname(__file__))
    if req.args.get('dl')!=None:
        target=secure_filename(req.args.get('dl'))
        if os.path.isfile(os.path.join("./fud/",target)):
            return send_file(os.path.join("./fud/",target),as_attachment = True)

    if req.method == 'POST':
        if 'upload' in req.files:
            req.files['upload'].save(os.path.join("./fud/",secure_filename(req.files['upload'].filename)))
        if 'delete' in req.form:
            target=secure_filename(req.form['delete'])
            os.path.isfile(os.path.join("./fud/",target))
            if os.path.isfile(os.path.join("./fud/",target)):os.remove(os.path.join("./fud/",target))
            
        
    return render_template_2("fud.html",FILES=htmlwalk())
