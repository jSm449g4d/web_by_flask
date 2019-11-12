# coding: utf-8
from flask import  render_template,redirect
import psutil 
import platform
import os 
def show(req):
    
    os.chdir(os.path.dirname(__file__))
    return render_template("/22.html",
    PLT_M=platform.processor(),
    CPU_F=psutil.cpu_freq(),
    CPU_P=psutil.cpu_percent(percpu=True),
    MEM_T=psutil.virtual_memory().total,
    MEM_U=psutil.virtual_memory().used,)
