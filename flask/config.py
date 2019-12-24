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

status="not_available"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
dir_db='./flask.sqlite3'
GCS_bucket="fb_gcs_bucket"
GCS_blob='flask.sqlite3'

try:#get_key
    storage_clienta = storage.Client.from_service_account_json("FirebaseAdminKey.json")
    status="access success"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
except:0

def render_template_2(dir,**kwargs):
    html=""
    with open(os.path.join("./templates/",dir),"r",encoding="utf-8") as f:
        html=f.read()
        for kw,arg in kwargs.items():
            html=html.replace("{{"+kw+"}}",arg)
    return render_template_string(html)

def show(req):
    status_GCS=status
    if req.method == 'POST':
        if "gcs_upload" in req.form and secure_filename(req.form["gcs_upload"])=="True":
            try:
                bucket= storage_clienta.get_bucket(GCS_bucket)
                bucket.blob(GCS_blob).upload_from_filename(dir_db)
                status_GCS="APP→GCS"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
            except:
                status_GCS="error: APP→×GCS"+datetime.now(pytz.UTC).strftime(" %Y/%m/%d %H:%M:%S (UTC)")
    return render_template_2("config.html",STATUS_GCS=status_GCS,DIR_DB=dir_db,GCS_BUCKET=GCS_bucket,GCS_BLOB=GCS_blob)

