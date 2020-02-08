# coding: utf-8
import psutil 
import platform
import os 
import wsgi_util
def show(req):
    return wsgi_util.render_template_2("22.html",
    PLT_M=platform.processor(),
    CPU_F=psutil.cpu_freq(),
    CPU_P=psutil.cpu_percent(percpu=True),
    MEM_T='{:,}'.format(psutil.virtual_memory().total),
    MEM_U='{:,}'.format(psutil.virtual_memory().used),)
