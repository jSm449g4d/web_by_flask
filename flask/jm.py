from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os 
from janome.tokenizer import Tokenizer
import gc

t = Tokenizer()#'./neologd'
def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def show(req):
    os.chdir(os.path.dirname(__file__))
    output=""
    if req.method == 'POST':
        if 'submit' in req.form and secure_filename(req.form['submit'])=="True":
            if 'text' in req.form:
                target=req.form['text'].translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
                ret=""
                for token in t.tokenize(target):
                    ret+=token.surface+","+token.part_of_speech+"<br>"
                #del t;gc.collect()
                output+=ret
        if 'change' in req.form and secure_filename(req.form['change'])=="True":
            if 'text' in req.form:
                target=req.form['text'].translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
                ret=""
                for token in t.tokenize(target):
                    ret+=token.surface+"_"+token.part_of_speech+"<br>"
                output+=ret
    return render_template_2("jm.html",OUTPUT=output)
