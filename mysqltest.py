#9th

### Under_Construction

#For security reasons, it is recommended to prevent external access to MySQL or the user
#The following MySQL commands were entered before running wsgi.py
#MySQL> CREATE DATABASE flaskdb DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
#MySQL> CREATE USER flaskuser@localhost IDENTIFIED BY 'krV93s44_9xzS';
#MySQL> GRANT ALL ON flaskdb.* to flaskuser@localhost;

from flask import  render_template_string
import os
import MySQLdb
import hashlib

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

conf={"host":"localhost","user":"flaskuser","password":"krV93s44_9xzS",
    "database":"flaskdb","charset":"utf8","autocommit":True,}



def init_flaskdb():
    con = MySQLdb.connect(**conf)
    cur = con.cursor()
    cur.execute("create table if not exists user (name varcahr(16),sha256 text)")

    cur.execute("show tables")
    row=str(cur.fetchall())
    cur.close()

    return row

#Development is frozen
def show_FREEZE(req):
    os.chdir(os.path.dirname(__file__))
    row="Under_Construction"
    #row=init_flaskdb()
    return render_template_2("mysqltest.html",CTZ=row)
