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
#from firebase_admin import storage

status_GCS="error"
FIREBASE="None"
dir_config_json='./config.json'
config_dict={"dir_db":'flask.sqlite3',"dir_gcp_key":"FirebaseAdminKey.json",
            "GCS_bucket":"fb_gcs_bucket","GCS_blob":"flask.sqlite3"}
iii=0

if os.path.exists(dir_config_json):
    with open(dir_config_json,"r",encoding="utf-8") as fp:config_dict=json.load(fp)    
else:
    with open(dir_config_json,"w",encoding="utf-8") as fp:json.dump(config_dict,fp)
    os.chmod(dir_config_json,0o777)


try:#GCS key→client
    storage_client = storage.Client.from_service_account_json(config_dict["dir_gcp_key"])
    status_GCS="access success"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
except:
    status_GCS="not_available"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
try:#Firebase key→client
    cred = firebase_admin.credentials.Certificate("FirebaseAdminKey.json")
    firebase_admin.initialize_app(cred)
    FIREBASE="available"
except:0

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def config_json_update(form={}):
    global config_dict
    if "status_GCS" in form:
        config_dict["status_GCS"]=secure_filename(form["status_GCS"])
    if "GCS_bucket" in form:
        config_dict["GCS_bucket"]=secure_filename(form["GCS_bucket"])
    if "GCS_blob" in form:
        config_dict["GCS_blob"]=secure_filename(form["GCS_blob"])
    if "dir_gcp_key" in form:
        config_dict["dir_gcp_key"]=secure_filename(form["dir_gcp_key"])
    with open(dir_config_json,"w+",encoding="utf-8") as fp:json.dump(config_dict,fp)
    os.chmod(dir_config_json,0o777)

def show(req):
    global status_GCS;global storage_client
    global iii;iii+=1
    if req.method == 'POST':
        if "gcs_upload" in req.form and secure_filename(req.form["gcs_upload"])=="True":
            try:
                storage_client.get_bucket(config_dict["GCS_bucket"]).blob(config_dict["GCS_blob"]).upload_from_filename(config_dict["dir_db"])
                status_GCS="APP→GCS"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
            except:
                status_GCS="error: APP→×GCS"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
        if "gcs_download" in req.form and secure_filename(req.form["gcs_download"])=="True":
            try:
                storage_client.get_bucket(config_dict["GCS_bucket"]).blob(config_dict["GCS_blob"]).download_to_filename(config_dict["dir_db"])
                status_GCS="GCS→APP"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
            except:
                status_GCS="error: GCS→×APP"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
        if "gcs_client_reload" in req.form and secure_filename(req.form["gcs_client_reload"])=="True":
            try:#get_key
                storage_client = storage.Client.from_service_account_json(config_dict["dir_gcp_key"])
                status_GCS="success gcs_client_reload"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
            except:
                status_GCS="error: ×gcs_client_reload"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
        #config_json_update(req.form)
        #↑Auth is Under construction
    return render_template_2("config.html",STATUS_GCS=status_GCS,DIR_DB=config_dict["dir_db"],GCS_BUCKET=config_dict["GCS_bucket"],
                            GCS_BLOB=config_dict["GCS_blob"],DIR_GCP_KEY=config_dict["dir_gcp_key"],COUNTER_M=str(iii))

