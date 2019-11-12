from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os 
import sqlite3
import hashlib
import datetime

def Display_Current_SQL(passwd=""):
    html=""
    #sqlite3
    con=sqlite3.connect(os.path.join("./flask.sqlite"),isolation_level = None)
    cur=con.cursor()
    cur.execute("create table if not exists nicoapi (sha256 text,url text,date datetime)")
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    orders=cur.execute("select * from nicoapi where sha256=\"%s\""%sha256).fetchall()
    cur.close();con.close()
    #add_texts_into_html
    for order in orders:
        html+="<tr><td class=\"flask_table\">"+str(order[1])+"</td>"
        html+="<td class=\"flask_table\">"+str(order[2])+"</td></tr>"#
    return html

def Order_Into_SQL(passwd="",order=""):
    #sqlite3
    con=sqlite3.connect(os.path.join("./flask.sqlite"),isolation_level = None)
    cur=con.cursor()
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    cur.execute("insert into nicoapi values(?,?,?)",[sha256,order,datetime.datetime.now()])
    cur.close();con.close()

def Clear_Order_SQL(passwd=""):
    #sqlite3
    con=sqlite3.connect(os.path.join("./flask.sqlite"),isolation_level = None)
    cur=con.cursor()
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    cur.execute("delete from nicoapi where sha256=\"%s\""%sha256)
    cur.close();con.close()

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def show(req):
    os.chdir(os.path.dirname(__file__))
    passwd=""
    urls="https://api.search.nicovideo.jp/api/v2/video/contents/search"
    if req.method == 'POST':
        if 'url' in req.form:#set_url
            urls=req.form['url']
        if 'pass' in req.form:#set_username
            passwd=secure_filename(req.form['pass'])
        if "launch" in req.form and secure_filename(req.form["launch"])=="True":
            Order_Into_SQL(passwd,urls)
        if "clear" in req.form and secure_filename(req.form["clear"])=="True":
            Clear_Order_SQL(passwd)

    orders=Display_Current_SQL(passwd)
    return render_template_2("nicoapi.html",ORDERS=orders,URL=urls,PASS=passwd)
