#9th
#plz check chmod -R 

from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os
import sqlite3
import hashlib

DataDir="./fud"

def htmlwalk():
    #sqlite3 
    con=sqlite3.connect(os.path.join("./flask.sqlite3"),isolation_level = None)
    cur=con.cursor()
    cur.execute("create table if not exists fub (name text unique,sha256 text)")
    wlks="\""+"\",\"".join(os.listdir(DataDir))+"\""#[A,B,C,...] -> "A","B","C",...
    cur.execute("delete from fub where name not in (%s)"%wlks)

    html=""
    wlks=os.listdir(DataDir)
    
    for wlk in wlks:
        sha256=cur.execute("select sha256 from fub where name=\"%s\""%wlk).fetchone()
        if sha256==None:continue#if not exist in table,be rejected
        html+="<tr><td><button name=\"delete\" value=\""+wlk+"\">DEL</button></td>"
        html+="<td><a class=\"file\" href=\"?dl="+wlk+"\">"+wlk+"</a></td>"
        html+="<td>"+str(sha256[0])+"</td></tr>"
    cur.close();con.close()
    return html

def sql_reg(name,passwd,mode=0):#confirmation->registration
    passwd=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    con=sqlite3.connect(os.path.join("./flask.sqlite3"),isolation_level = None)
    cur=con.cursor()
    sha256=cur.execute("select sha256 from fub where name=\"%s\""%name).fetchone()
    #confirmation_mode
    if mode==0:
        if sha256==None:
            print("not_registrated!");cur.close();con.close();return 0
        elif str(sha256[0])!=passwd:print("rejected!");cur.close();con.close();return 0
        else :print("accepted!");cur.close();con.close();return 1
    #registration
    if sha256!=None:
        if str(sha256[0])!=passwd:print("rejected!");cur.close();con.close();return 0
    try :cur.execute("insert into fub values(\"%s\",\"%s\")"%(name,passwd))
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
    if not os.path.exists(DataDir):os.mkdir(DataDir)
    passwd=""
    #GET
    if req.args.get('dl')!=None:
        target=req.args.get('dl').translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
        return send_file(os.path.join(DataDir,target),as_attachment = True)
    #POST
    if req.method == 'POST':
        if 'pass' in req.form:
            passwd=secure_filename(req.form['pass'])
        if 'upload_file' in req.form and 'upload' in req.files:
            target=req.files['upload'].filename.translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
            if sql_reg(target,passwd,mode=1)!=0:
                req.files['upload'].save(os.path.join(DataDir,target))
        if 'delete' in req.form:
            target=req.form['delete'].translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
            if sql_reg(target,passwd,mode=0)!=0:
                os.remove(os.path.join(DataDir,target))
            
    return render_template_2s("fud.html",FILES=htmlwalk(),PASS=passwd)
