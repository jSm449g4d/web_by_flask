from flask import  render_template_string,send_file
from werkzeug.utils import secure_filename
import os 
import sqlite3
import hashlib
import datetime
import zipfile
import subprocess
import shutil
import psutil

DataDir="./nicoapi"

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
        html+="<tr><td>"+str(order[1])+"</td>"
        html+="<td>"+str(order[2]).split(".")[0]+"</td></tr>"
    return html

def Order_Into_SQL(passwd="",order=""):
    #sqlite3
    con=sqlite3.connect(os.path.join("./flask.sqlite"),isolation_level = None)
    cur=con.cursor()
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    if cur.execute("select * from nicoapi where sha256=? and url=?",[sha256,order]).fetchone()==None:
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

def about_files(passwd=""):
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    try:files=os.listdir(os.path.join(DataDir,sha256))
    except:return "Not_Exist","Not_Exist"
    size = sum([os.path.getsize(os.path.join(DataDir,sha256,f)) for f in files])
    return str(len(files))+"[Files]",'{:,}'.format(size)+"[Byte]"

def download_files(passwd=""):
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    try:files=os.listdir(os.path.join(DataDir,sha256))
    except:return render_template_string("<a href=\"\">back</a>")
    tempfile=os.path.join(DataDir,sha256,"download.zip")
    try:zip = zipfile.ZipFile(tempfile, 'a', zipfile.ZIP_DEFLATED)
    except:zip = zipfile.ZipFile(tempfile, 'w', zipfile.ZIP_DEFLATED)
    for f in files:
        if f.split(".")[-1]=="zip":continue
        zip.write(os.path.join(DataDir,sha256,f),f)
        os.remove(os.path.join(DataDir,sha256,f))
    zip.close()

    return send_file(tempfile,as_attachment = True)

def delete_files(passwd=""):
    sha256=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    try:shutil.rmtree(os.path.join(DataDir,sha256))
    except:return
    
def check_nicoapigo_status():
    for proc in psutil.process_iter():
        if 'nicoapi' in proc.name():return "Running"
    return "Stopping"

def fields_to_html_text_forms(id,prm="",val="",readonly="False"):
    html="<tr>"
    html+="<td><input type=\"text\" name=\"field1_"+str(id)+"\" value=\""+prm+"\" class=\"form-control form-control-sm\""
    if readonly=="True":html+=" readonly"
    html+="></td>"
    html+="<td><input type=\"text\" name=\"field2_"+str(id)+"\" value=\""+val+"\" class=\"form-control form-control-sm\">"
    html+="<input type=\"hidden\" name=\"field3_"+str(id)+"\" value=\""+readonly+"\"></td>"
    html+="</tr>"
    return html

def fill_default_fields(url=""):
    if "https://api.search.nicovideo.jp/api/v2/video/contents/search" in url:
        html =fields_to_html_text_forms(0,"q","ゆっくり解説","True")
        html+=fields_to_html_text_forms(1,"targets","title,description,tags","True")
        html+=fields_to_html_text_forms(2,"fields","contentId,title,description,tags","True")
        html+=fields_to_html_text_forms(3,"_sort","viewCounter","True")
        html+=fields_to_html_text_forms(4,"_limit","100")
        html+=fields_to_html_text_forms(5,"_offset","AAAAAX")
        fields_command="AAAAAX_0_1601_100"

    elif "https://api.search.nicovideo.jp/api/v2/live/contents/search" in url:
        html =fields_to_html_text_forms(0,"q","ゆっくり解説","True")
        html+=fields_to_html_text_forms(1,"targets","title,description,tags","True")
        html+=fields_to_html_text_forms(2,"fields","contentId,title,description,tags","True")
        html+=fields_to_html_text_forms(3,"_sort","viewCounter","True")
        html+=fields_to_html_text_forms(4,"_limit","100")
        html+=fields_to_html_text_forms(5,"_offset","AAAAAX")
        fields_command="AAAAAX_0_1601_100"
    
    elif "https://api.syosetu.com/novelapi/api" in url:
        html =fields_to_html_text_forms(0,"gzip","5")
        html+=fields_to_html_text_forms(1,"out","json")
        html+=fields_to_html_text_forms(2,"lim","499")
        html+=fields_to_html_text_forms(3,"st","AAAAAX")
        fields_command="AAAAAX_1_2000_499"

    else :
        html=fields_to_html_text_forms(0)
        fields_command=""
    return html,fields_command




#Development is frozen
def show(req):
    os.chdir(os.path.join("./",os.path.dirname(__file__)))
    if not os.path.exists(DataDir):os.mkdir(DataDir)
    #declare
    urls="https://api.search.nicovideo.jp/api/v2/video/contents/search"
    query=""
    passwd=""
    nicoapigo_s="non check"
    fields=""
    fields_c=""#fields_command
    if req.method == 'POST':
        if 'url' in req.form:
            urls=req.form['url'].translate(str.maketrans("\"\'<>`?;",'_______'))#Not_secure_filename!
        if 'query' in req.form:
            query=req.form['query'].translate(str.maketrans("\"\'<>`?;",'_______'))#Not_secure_filename!
        if 'pass' in req.form:
            passwd=secure_filename(req.form['pass'])
        if 'fields_c' in req.form:
            fields_c=secure_filename(req.form["fields_c"])
        #read_query_forms
        f1=[req.form[j].translate(str.maketrans("\"\'\\/<>%`?;",'__________')) for j in req.form if "field1_" in j]#Not_secure_filename!
        f2=[req.form[j].translate(str.maketrans("\"\'\\/<>%`?;",'__________')) for j in req.form if "field2_" in j]#Not_secure_filename!
        f3=[secure_filename(req.form[j]) for j in req.form if "field3_" in j]
        if "fields_ad" in req.form:
            if secure_filename(req.form['fields_ad'])=="add":
                f1.append("");f2.append("");f3.append("False")
            if secure_filename(req.form['fields_ad'])=="del" and 1<len(f1) and f3[-1]!="True":
                f1.pop(-1);f2.pop(-1);f3.pop(-1)
        for i in range(len(f1)):
            fields+=fields_to_html_text_forms(i,f1[i],f2[i],f3[i])
            query+="&"+f1[i]+"="+f2[i]
        if "launch" in req.form and secure_filename(req.form["launch"])=="True":
            try:
                for x in fields_c.split():
                    if len(x.split("_"))==4:#a_b_c_d → [a for a in range(b,c,d)]
                        if (int(x.split("_")[2])-int(x.split("_")[1]))/int(x.split("_")[3])>5000:
                            print("\nerror:Too many order");continue
                        for Y in [y for y in range(int(x.split("_")[1]),int(x.split("_")[2]),int(x.split("_")[3]))]:
                            Order_Into_SQL(passwd,urls+"?"+query.replace(x.split("_")[0],str(Y)))
                #If there is no command.
                if len(fields_c.split())==0:
                    Order_Into_SQL(passwd,urls+"?"+query)
            except:print("Order_Into_SQL:error")        
        #Reload query for clearing query's params which ware added by html_text_forms
        if 'query' in req.form:
            query=req.form['query'].translate(str.maketrans("\"\'<>`?;",'_______'))#Not_secure_filename!
        if "clear" in req.form and secure_filename(req.form["clear"])=="True":
            Clear_Order_SQL(passwd)
        if "delete" in req.form and secure_filename(req.form["delete"])=="True":
            delete_files(passwd)
        if "download" in req.form and secure_filename(req.form["download"])=="True":
            return download_files(passwd)
            #Frozen
        #if "nicoapigo" in req.form and secure_filename(req.form["nicoapigo"])=="True":
        #    try:subprocess.run(['go','run',os.path.join(os.getcwd(),'nicoapi.go')])
        #    except:print("Faild to launch nicoapi.go")
        #    nicoapigo_s=check_nicoapigo_status()
        #if "nicoapigokill" in req.form and secure_filename(req.form["nicoapigokill"])=="True":
        #    try:
        #        for proc in psutil.process_iter():
        #            if 'nicoapi' in proc.name():proc.terminate()
        #    except:print("Faild to Terminate nicoapi.go")
        #    nicoapigo_s=check_nicoapigo_status()
        if "nicoapigostatus" in req.form and secure_filename(req.form["nicoapigostatus"])=="True":
            nicoapigo_s=check_nicoapigo_status()
        
        #select_API_endpoint is a command which cause to reset forms as like no POST
        if "select_API_endpoint" in req.form:
            urls=req.form["select_API_endpoint"].translate(str.maketrans("\"\'<>`?;",'_______'))#Not_secure_filename!
            fields,fields_c=fill_default_fields(urls)
    else :
        fields,fields_c=fill_default_fields(urls)
    

    orders=Display_Current_SQL(passwd)
    _,size_files=about_files(passwd)
    return render_template_2("nicoapi.html",ORDERS=orders,URL=urls,QUERY=query,PASS=passwd,\
    SIZE_FILES=size_files,NICOAPIGO_S=nicoapigo_s,FIELDS=fields,FIELDS_C=fields_c)
