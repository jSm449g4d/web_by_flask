#9th
#plz check chmod -R 

from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os 
import sqlite3
import hashlib

os.chdir(os.path.dirname(__file__))
DataDir="./fud"

def htmlwalk():
    #sqlite3 
    con=sqlite3.connect(os.path.join(DataDir,"fud.sqlite"),isolation_level = None)
    cur=con.cursor()
    cur.execute("create table if not exists protected (name text unique,sha256 text)")
    wlks="\""+"\",\"".join(os.listdir(DataDir))+"\""#[A,B,C,...] -> "A","B","C",...
    cur.execute("delete from protected where name not in (%s)"%wlks)

    html=""
    wlks=os.listdir(DataDir)
    
    for wlk in wlks:
        html+="<li>"+"<a class=\"file\" href=\"?dl="+wlk+"\">"+wlk+"</a>\t"
        html+="<button name=\"delete\" value=\""+wlk+"\">DEL</button>"
        sha256=cur.execute("select sha256 from protected where name=\"%s\""%wlk).fetchone()
        if sha256!=None:sha256=sha256[0]
        html+="sha256:"+str(sha256)+"</li>"
    cur.close();con.close()
    return html

def sql_reg(name,passwd,mode=0):#confirmation->registration
    passwd=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    con=sqlite3.connect(os.path.join(DataDir,"fud.sqlite"),isolation_level = None)
    cur=con.cursor()
    cur.execute("create table if not exists protected (name text unique,sha256 text)")
    sha256=cur.execute("select sha256 from protected where name=\"%s\""%name).fetchone()
    if sha256!=None:sha256=sha256[0]
    #registrated and mismatch -> rejected!
    if sha256!=None and str(sha256)!=passwd:
        print("rejected!");cur.close();con.close();return 0
    #confirmation_mode or non_registering -> accepted!
    if mode==0 or passwd==hashlib.sha256().hexdigest():
        cur.close();con.close();return 1
    #registration
    try :cur.execute("insert into protected values(\"%s\",\"%s\")"%(name,passwd))
    except:print("overwrite!");cur.close();con.close();return 2
    print("success!");cur.close();con.close();return 2

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def show(req):    
    os.chdir(os.path.dirname(__file__))
    #GET
    if req.args.get('dl')!=None:
        target=secure_filename(req.args.get('dl'))
        return send_file(os.path.join(DataDir,target),as_attachment = True)
    #POST
    if req.method == 'POST':
        if 'upload_file' in req.form and 'upload' in req.files:
            target=secure_filename(req.files['upload'].filename)
            if sql_reg(target,req.form['pass'],mode=1)!=0:
                req.files['upload'].save(os.path.join(DataDir,target))
        if 'delete' in req.form:
            target=secure_filename(req.form['delete'])
            if sql_reg(target,req.form['pass'],mode=0)!=0:
                os.remove(os.path.join(DataDir,target))
            
    return render_template_2("fud.html",FILES=htmlwalk())
