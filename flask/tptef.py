from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os 
import sqlite3
import hashlib
import datetime

def Display_Current_SQL(room=""):
    html=""
    #sqlite3
    con=sqlite3.connect(os.path.join("./flask.sqlite"),isolation_level = None)
    cur=con.cursor()
    cur.execute("create table if not exists tptef (room text,user text,remark text,sha256 text,date datetime)")
    orders=cur.execute("select * from tptef where room=\"%s\""%room).fetchall()
    cur.close();con.close()
    #add_texts_into_html
    for order in orders:
        html+="<tr><td class=\"flask_table\">"+str(order[1])+"</td>"
        html+="<td class=\"flask_table\">"+str(order[2])+"</td>"
        #Display 48 characters of sha256
        html+="<td class=\"flask_table\" style=\"font-size: 12px;\">"+str(order[3])[:16]+"<br>"+str(order[3])[16:32]+\
        "<br>"+str(order[3])[32:48]+"<br>"+str(order[3])[48:]+"</td>"
        #timestamp
        html+="<td class=\"flask_table\" style=\"font-size: 12px;\">"+str(order[4]).split(".")[0]+"</td></tr>"
    return html

def Order_Into_SQL(room="",user="",remark="",passwd=""):
    #sqlite3
    con=sqlite3.connect(os.path.join("./flask.sqlite"),isolation_level = None)
    cur=con.cursor()
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    cur.execute("insert into tptef values(?,?,?,?,?)",[room,user,remark,sha256,datetime.datetime.now()])
    cur.close();con.close()

def Clear_Order_SQL(passwd=""):
    #sqlite3
    con=sqlite3.connect(os.path.join("./flask.sqlite"),isolation_level = None)
    cur=con.cursor()
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    cur.execute("delete from tptef where sha256=\"%s\""%sha256)
    cur.close();con.close()

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def show(req):
    os.chdir(os.path.join("./",os.path.dirname(__file__)))
    room=""
    user=""
    remark=""
    passwd=""
    if req.method == 'POST':
        if 'room' in req.form:
            room=req.form['room'].translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
        if 'user' in req.form:
            user=req.form['user'].translate(str.maketrans("\"\'\\/<>%`?;",'__________'))#Not_secure_filename!
        if 'remark' in req.form:
            remark=req.form['remark'].translate(str.maketrans("\"\'\\/<>%`?;",'””￥_〈〉％”？；'))#Not_secure_filename!
        if 'pass' in req.form:
            passwd=secure_filename(req.form['pass'])
        if "launch" in req.form and secure_filename(req.form["launch"])=="True":
            Order_Into_SQL(room,user,remark,passwd)
        if "clear" in req.form and secure_filename(req.form["clear"])=="True":
            Clear_Order_SQL(passwd)

    orders=Display_Current_SQL(room)
    return render_template_2("tptef.html",ORDERS=orders,ROOM=room,USER=user,REMARK=remark,PASS=passwd)
