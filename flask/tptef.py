from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os
import hashlib
import datetime
import pytz
from firebase_admin import auth
from firebase_admin import firestore
import wsgi
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3


Base = declarative_base()
class tptef_table(Base):
    __tablename__ = 'tptef'
    room=Column(String(64))
    user=Column(String(64))
    remark=Column(String(256))
    sha256=Column(String(32))
    date = Column(String(64),primary_key= True)

def Display_Current_SQL(room=""):
    html=""
    try:
        session = sessionmaker(bind=wsgi.dbengine)()
        Base.metadata.create_all(wsgi.dbengine)
        session.add(testtable(room="sqlarchemytst",user ="",remark="tst",sha256=hashlib.sha256("")
                            ,date =datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)"))
        aaa=session.filter(tptef_table.room == room)
        session.commit()
        session.close()
        for i in aaa:
            html+=i+"<br>"
    except:
        return "DB_error"
    
    
    
    cur.execute("create table if not exists tptef (room text,user text,remark text,sha256 text,date datetime)")
    orders=cur.execute("select * from tptef where room=\"%s\""%room).fetchall()
    cur.close();con.close()
    #add_texts_into_html
    for order in orders:
        html+="<tr><td>"+str(order[1])+"</td>"
        html+="<td>"+str(order[2])+"</td>"
        #Display 48 characters of sha256
        html+="<td style=\"font-size: 12px;\">"+str(order[3])[:16]+"<br>"+str(order[3])[16:32]+\
        "<br>"+str(order[3])[32:48]+"<br>"+str(order[3])[48:]+"</td>"
        #timestamp
        html+="<td style=\"font-size: 12px;\">"+str(order[4]).split(".")[0]+"</td></tr>"
    return html

def Order_Into_SQL(room="",user="",remark="",passwd=""):
    #sqlite3
    con=sqlite3.connect(os.path.join("./flask.sqlite3"),isolation_level = None)
    cur=con.cursor()
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    cur.execute("insert into tptef values(?,?,?,?,?)",[room,user,remark,sha256,datetime.datetime.now()])
    cur.close();con.close()

def Clear_Order_SQL(passwd=""):
    #sqlite3
    con=sqlite3.connect(os.path.join("./flask.sqlite3"),isolation_level = None)
    cur=con.cursor()
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    cur.execute("delete from tptef where sha256=\"%s\""%sha256)
    cur.close();con.close()

def show(req):
    room=""
    user=""
    remark=""
    passwd=""
    fbtoken=""
    if req.method == 'POST':
        if "fbtoken" in req.form:fbtoken=secure_filename(req.form["fbtoken"])#Firebase_Token_keep
        
        if 'room' in req.form:
            room=req.form['room'].translate(str.maketrans("","","\"\'\\/<>%`?;"))#Not_secure_filename!
        if 'user' in req.form:
            user=req.form['user'].translate(str.maketrans("","","\"\'\\/<>%`?;"))#Not_secure_filename!
        if 'remark' in req.form:
            remark=req.form['remark'].translate(str.maketrans("\"\'\\/<>%`?;",'””￥_〈〉％”？；'))#Not_secure_filename!
        if 'pass' in req.form:
            passwd=secure_filename(req.form['pass'])
        if "launch" in req.form and secure_filename(req.form["launch"])=="True":
            Order_Into_SQL(room,user,remark,passwd)
        if "clear" in req.form and secure_filename(req.form["clear"])=="True":
            Clear_Order_SQL(passwd)

    orders=Display_Current_SQL(room)
    return wsgi.render_template_2("tptef.html",ORDERS=orders,ROOM=room,USER=user,REMARK=remark,PASS=passwd)
