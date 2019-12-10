from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os 
from janome.tokenizer import Tokenizer
import gc
import certifi
import urllib3
import json

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def FaaS_janome(url="",fields={}):
    ret=""
    if url=="":#fallback
        t = Tokenizer()#'./neologd'
        if 'speech' in fields:
            target=fields['speech'].translate(str.maketrans("\"\'\\/<>%`?;",'””￥_〈〉％”？；'))
            target=target.translate(str.maketrans(", ",'__'))
            for token in t.tokenize(target):
                ret+=token.part_of_speech.split(',')[0]+","
            del t;gc.collect();return ret.strip(',')
        if 'surface' in fields:
            target=fields['surface'].translate(str.maketrans("\"\'\\/<>%`?;",'””￥_〈〉％”？；'))
            target=target.translate(str.maketrans(", ",'__'))
            for token in t.tokenize(target):
                ret+=token.surface+","
            del t;gc.collect();return ret.strip(',')
        if 'phonetic' in fields:
            target=fields['phonetic'].translate(str.maketrans("\"\'\\/<>%`?;",'””￥_〈〉％”？；'))
            target=target.translate(str.maketrans(", ",'__'))
            for token in t.tokenize(target):
                ret+=token.phonetic+","
            del t;gc.collect();return ret.strip(',')
    https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where(),headers={})
    html=https.request('POST',url,
    body=json.dumps(fields),headers={'Content-Type': 'application/json'})
    return html.data.decode('utf-8').translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!

def show(req):
    os.chdir(os.path.dirname(__file__))
    output=""
    endpoint="https://us-central1-crack-atlas-251509.cloudfunctions.net/janome_banilla"
    if req.method == 'POST':
        if 'endpoint' in req.form:
            endpoint=req.form['endpoint'].translate(str.maketrans("\"\'<>`?;",'_______'))#Not_secure_filename!

        if 'submit' in req.form and secure_filename(req.form['submit'])=="True":
            if 'text' in req.form:
                target=req.form['text'].translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
                output+=FaaS_janome(endpoint,fields={"surface":target})+"<br>"
                output+=FaaS_janome(endpoint,fields={"speech":target})+"<br>"
                output+=FaaS_janome(endpoint,fields={"phonetic":target})

        if 'change' in req.form and secure_filename(req.form['change'])=="True":
            if 'text' in req.form:
                target=req.form['text'].translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
                ret=FaaS_janome(endpoint,fields={"surface":target})
                output+=ret
        
        #if 'dlsource' in req.form and secure_filename(req.form['dlsource'])=="True":
        #    return send_file(os.path.join(DataDir,target),as_attachment = True)

    return render_template_2("jm.html",OUTPUT=output,ENDPOINT=endpoint)
