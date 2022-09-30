import json
from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from app01.tasks.update_DB import update
from tempfile import mkstemp
from os import fdopen,unlink,kill
import signal
from subprocess import Popen
from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect

import os
from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModeForm
from app01 import models
import time
def city_list(request):
    queryset = models.City.objects.all()
    for i in queryset:
        print(i)
    for i in range(20):
        print(i)
        time.sleep(5)
    return HttpResponse("...")

def test(request):
    print("TEST")
    city_list(request)
    resultj={"result":True}
    return JsonResponse({"result":True})

def test1(request):
# def startjob(request):
    content={
        "result_str":'Not running a job.'+ '<p><a href="/test/">Start a new one?</a>'
    }
    if not request.session.has_key("job"):
        outfd,outname=mkstemp()
        request.session["jobfile"]=outname
        outfile=fdopen(outfd,"a+")
        proc=Popen("python myjob.py", shell=True,stdout=outfile)
        request.session["job"]=proc.pid
        print("PPPP",proc.pid)
        print("FFF",request.session["jobfile"])
        return render(request,"test.html",content)
    else:
        filename=request.session["jobfile"]


        results = open(filename)
        lines = results.readlines()
        print("linesSSSSSSS", lines)
        print("TTTTTTTTT")
        content["result_str"] = lines +   ['<p><a href="/test/del/">Terminate?</a>']

        return render(request,"test.html",content)


def rmjob(request):
    if request.session.has_key("job"):
        job=request.session["job"]
        filename=request.session["jobfile"]
        try:
            #kill(job,signal.SIGKILL)
            unlink(filename)
        except OSError as e:
            pass
        del request.session['job']
        del request.session['jobfile']
    return HttpResponseRedirect('/test/')  # start a new one