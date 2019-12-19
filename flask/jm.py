from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os 
from janome.tokenizer import Tokenizer
import gc
import certifi
import urllib3
import json
import asyncio
import threading
import random
from urllib import parse
import re
import neologdn
import random

jmloop = asyncio.new_event_loop()

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
    try:html=https.request('POST',url,
    body=json.dumps(fields),headers={'Content-Type': 'application/json'})
    except: return "ERROR:invalid endpoint"
    return html.data.decode('utf-8').translate(str.maketrans("","","\"\'\\/<>%`?;"))#Not_secure_filename!

def FaaS_wakeup(url="",q="warmup=True"):
    https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where(),headers={
        "User-Agent":"Janome_doe"})
    try:https.request('GET',url+"?"+q)
    except: return ""
    return 

def web_rand(url="",fields={}):
    https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where(),
    headers={"User-Agent":"Janome_doe"})
    try:html=https.request('POST',str(url).split("?")[0]+"?"+parse.quote(str(url).split("?")[1],safe="=&-"))
    except: print("err");return "ERROR:invalid endpoint"
    html=html.data.decode('utf-8').translate(str.maketrans("","","\"\'\\/<>%`?;"))#Not_secure_filename!
    return neologdn.normalize(html).translate(str.maketrans("","","_:| ～-#"))

def show(req):
    os.chdir(os.path.join("./",os.path.dirname(__file__)))
    output=""
    endpoint="https://us-central1-crack-atlas-251509.cloudfunctions.net/janome_banilla"
    random_art="https://api.syosetu.com/novelapi/api?of=t-w-s&lin=10&st=_RANDINT2000_"
    change_prob=0.2

    #FaaS wakeup
    threading.Thread(name='t1', target=FaaS_wakeup, kwargs={'url': endpoint}).start()
    if req.method == 'POST':
        if 'endpoint' in req.form:
            endpoint=req.form['endpoint'].translate(str.maketrans("","","\"\'<>`;"))#Not_secure_filename!
        if 'random_art' in req.form:
            random_art=req.form['random_art'].translate(str.maketrans("","","\"\'<>`;"))#Not_secure_filename!
        if 'change_prob' in req.form:
            change_prob=float(secure_filename(req.form['change_prob']))
        if 'submit' in req.form and secure_filename(req.form['submit'])=="True":
            if 'text' in req.form:
                target=req.form['text'].translate(str.maketrans("","","\"\'\\/<>%`?;"))#Not_secure_filename!
                output+=FaaS_janome(endpoint,fields={"surface":target})+"<br>"
                output+=FaaS_janome(endpoint,fields={"speech":target})+"<br>"
                output+=FaaS_janome(endpoint,fields={"phonetic":target})"<br>"
                output+=FaaS_janome(endpoint,fields={"speech2":target})"<br>"

        if 'noun' in req.form and secure_filename(req.form['noun'])=="True":
            tmp=""#_RANDINTxxx_ → randint(1,xxx) on url
            for i,txt in enumerate(random_art.split("_RANDINT")):
                if i==0:tmp=txt;continue
                tmp+=str(random.randint(1,int(txt.split("_")[0])))
                if 1<len(txt.split("_")):tmp+=''.join(txt.split("_")[1:])
            rand_text=web_rand(tmp)
            rand_text_surface=FaaS_janome(endpoint,fields={"surface":rand_text})
            rand_text_speech=FaaS_janome(endpoint,fields={"speech":rand_text})
            rand_noun=set(["佐藤"])
            rand_verb=set(["送る"])
            for i in range(len(rand_text_speech.split(","))):
                if rand_text_speech.split(",")[i]=="名詞":rand_noun.add(rand_text_surface.split(",")[i])
                if rand_text_speech.split(",")[i]=="動詞":rand_verb.add(rand_text_surface.split(",")[i])
            for _ in range(15):output+=random.choice(list(rand_noun))+" "
            output+="<br>"
            for _ in range(15):output+=random.choice(list(rand_verb))+" "
            output+="<br>"
                    
        if 'change' in req.form and secure_filename(req.form['change'])=="True":
            if 'text' in req.form:
                target=req.form['text'].translate(str.maketrans("","","\"\'\\/<>%`?;"))#Not_secure_filename!
                text_surface=FaaS_janome(endpoint,fields={"surface":target})
                text_speech=FaaS_janome(endpoint,fields={"speech":target})

                tmp=""#_RANDINTxxx_ → randint(1,xxx) on url
                for i,txt in enumerate(random_art.split("_RANDINT")):
                    if i==0:tmp=txt;continue
                    tmp+=str(random.randint(1,int(txt.split("_")[0])))
                    if 1<len(txt.split("_")):tmp+=''.join(txt.split("_")[1:])
                
                rand_text=web_rand(tmp)
                rand_text_surface=FaaS_janome(endpoint,fields={"surface":rand_text})
                rand_text_speech=FaaS_janome(endpoint,fields={"speech":rand_text})
                rand_noun=set(["佐藤"])
                rand_verb=set(["送る"])
                for i in range(len(rand_text_speech.split(","))):
                    if rand_text_speech.split(",")[i]=="名詞":rand_noun.add(rand_text_surface.split(",")[i])
                    if rand_text_speech.split(",")[i]=="動詞":rand_verb.add(rand_text_surface.split(",")[i])

                for i in range(len(text_surface.split(","))):
                    if text_speech.split(",")[i]=="名詞" and change_prob>random.random():
                        output+=random.choice(list(rand_noun));continue
                    output+=text_surface.split(",")[i]
        
    return render_template_2("jm.html",OUTPUT=output,ENDPOINT=endpoint,RANDOM_ART=random_art,CHANGE_PROB=str(change_prob))
