import os
from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModeForm
from app01 import models
from app01.tasks.Kitbunder_build_check import kitbunds_test
import time
from tempfile import mkstemp
from os import fdopen,unlink,kill
from subprocess import Popen


def release_tasks(request):
    title ="Release tasks"
    bug_list = [3785542, 3782813,3782592,3775740]
    queryset = models.NvBug.objects.filter(BugId__in=bug_list)
    result_list = []
    result_dict= {
        "title":title,
        "bug_list":bug_list,
        "version" :None,
        "result_list" :result_list,
        "queryset": queryset,
    }

    if request.method == "POST":
        print(request.POST.get("version"))
        version=request.POST.get("version")
        #result_list=kitbunds_test(version)
        cmd = "python app01/tasks/Kitbunder_build_check.py -v "+ version
        print(cmd)
        outfd, outname = mkstemp()
        request.session["jobfile"] = outname
        outfile = fdopen(outfd, "a+")
        proc = Popen(cmd, shell=True, stdout=outfile)
        request.session["kitbunds"] = proc.pid

        print("PPPPPPPPPPPPPPPPPPPPPPPP",proc.pid)
        time.sleep(5)
        filename = request.session["jobfile"]

        results = open(filename)
        lines = results.readlines()

        result_list.extend(lines)
        print("WWWWWWWWW5 second")
        print(result_dict["result_list"])

        return render(request, "release_tasks.html", result_dict)


    if request.method == "GET" and not request.session.has_key("kitbunds"):
        print("GGGGGG")
        return render(request, "release_tasks.html",result_dict)
    if request.session.has_key("kitbunds"):
        print("XXXXXXXXXXXXXXXXXXXX")
        filename = request.session["jobfile"]
        print(filename)
        results = open(filename)
        lines = results.readlines()

        result_list.extend(lines)

    return render(request, "release_tasks.html",result_dict)

def release_del(request):
    if request.session.has_key("kitbunds"):
        job=request.session["kitbunds"]

        try:
            if request.session.has_key("jobfile"):
                filename = request.session["jobfile"]
                unlink(filename)
                del request.session['jobfile']
                # kill(job,signal.SIGKILL)
        except OSError as e:
            pass
        del request.session['kitbunds']

    return redirect("/release/tasks/")