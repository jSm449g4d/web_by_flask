#This is Config file
#plz rewrite this file your env

from flask import  render_template_string,redirect
from werkzeug.utils import secure_filename
import psutil 
import platform
import os
from google.cloud import storage
from datetime import datetime
import pytz
import json
import firebase_admin
from firebase_admin import auth,firestore
from urllib import parse
import wsgi_util
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

status_GCS="error"
dir_config_json='./config.json'
config_dict={"dir_db":'flask.sqlite3',
            "form_gcs_uri":"gs://fb_gcs_bucket/flask.sqlite3",
            "FB_admin_uid":"1GYEMV6s2OWU9dR2cXCntSlR2op2"}
iii=0

if os.path.exists(dir_config_json):
    with open(dir_config_json,"r",encoding="utf-8") as fp:config_dict=json.load(fp)    
else:
    with open(dir_config_json,"w",encoding="utf-8") as fp:json.dump(config_dict,fp)
    os.chmod(dir_config_json,0o777)

try:#GCS key→client
    storage_client = storage.Client.from_service_account_json("FirebaseAdmin_Key.json")
    status_GCS="access success"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
except:
    status_GCS="not_available"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
try:#Firebase key→client
    cred = firebase_admin.credentials.Certificate("FirebaseAdmin_Key.json")
    firebase_admin.initialize_app(cred)
except:0

def config_json_update(form={}):
    global config_dict
    if "status_GCS" in form:
        config_dict["status_GCS"]=secure_filename(form["status_GCS"])
    if "form_gcs_uri" in form:
        config_dict["form_gcs_uri"]=form["form_gcs_uri"].translate(str.maketrans("","","\"\'<>`;"))#Not_secure_filename!
    with open(dir_config_json,"w+",encoding="utf-8") as fp:json.dump(config_dict,fp)
    os.chmod(dir_config_json,0o777)

def html_create_recode(title="",data="",color="navy"):
    return "<tr><td style=\"color:"+color+";\">"+title+"</td><td style=\"color:"+color+";\">"+data+"</td></tr>"
    

Base = declarative_base()
class testtable(Base):
    __tablename__ = 'test2'
    id = Column(Integer,primary_key = True)
    date = Column(String(255))
    temperature = Column(Integer)

def show(req):
    global status_GCS,storage_client,config_dict;
    global iii;iii+=1
    status_table=html_create_recode("access_counter",str(iii))
    clearance=0#0:non-login,1:general,2:admin
    if req.method == 'POST':
        #Check Auth
        if "fbtoken" in req.form:fbtoken=secure_filename(req.form["fbtoken"])#Firebase_Token_keep
        try:#User authentication
            if config_dict["FB_admin_uid"]==firebase_admin.auth.verify_id_token(fbtoken)["uid"]:
                config_json_update(req.form)
                status_table+=html_create_recode("Authority","<b>Admin</b>");clearance=2                
            else :
                status_table+=html_create_recode("Authority","general");clearance=1
        except:
            status_table+=html_create_recode("Authority","Non-login");clearance=0
        #/Check Auth
        #Operation
        if "gcs_upload" in req.form and secure_filename(req.form["gcs_upload"])=="True":
            if clearance==2:
                try:
                    storage_client.get_bucket(parse.urlsplit(config_dict["form_gcs_uri"])[1])\
                    .blob(parse.urlsplit(config_dict["form_gcs_uri"])[2].strip("/")).upload_from_filename(config_dict["dir_db"])
                    status_GCS="APP→GCS"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
                except:
                    status_GCS="APP→×GCS"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
            else:status_table+=html_create_recode("APP→×GCS","The operation Don't allowed for your clearance.",color="red")
        if "gcs_download" in req.form and secure_filename(req.form["gcs_download"])=="True":
            if clearance==2:
                try:
                    storage_client.get_bucket(parse.urlsplit(config_dict["form_gcs_uri"])[1])\
                    .blob(parse.urlsplit(config_dict["form_gcs_uri"])[2].strip("/")).download_to_filename(config_dict["dir_db"])
                    status_GCS="GCS→APP"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
                except:
                    status_GCS="GCS→×APP"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
            else:status_table+=html_create_recode("GCS→×APP","The operation Don't allowed for your clearance.",color="red")
        if "gcs_client_reload" in req.form and secure_filename(req.form["gcs_client_reload"])=="True":
            if clearance==1 or clearance==2:
                try:#get_key
                    storage_client = storage.Client.from_service_account_json("FirebaseAdmin_Key.json")
                    status_GCS="reload:gcs_client"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
                except:
                    status_GCS="×gcs_client_reload"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
            else:status_table+=html_create_recode("×gcs_client_reload","The operation Don't allowed for your clearance.",color="red")
            
        if "fb_fs" in req.form and secure_filename(req.form["fb_fs"])=="True":
            db = firestore.client()
            resp=db.collection('users').document('alovelace').get().to_dict()
            status_table+=html_create_recode("Firestore",json.dumps(resp))
        if "Resource_Reload" in req.form and secure_filename(req.form["Resource_Reload"])=="True":
            wsgi_util.Resource_Reload()
    return wsgi_util.render_template_2("config.html",STATUS_GCS=status_GCS,DIR_DB=config_dict["dir_db"],
                            form_gcs_uri=config_dict["form_gcs_uri"],STATUS_TABLE=status_table)

