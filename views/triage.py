import json
from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from app01.utils.bootstrap import BootStrapModeForm
import os
from app01 import models
from app01.utils.pageaction import PageInaction
from app01.tasks.run_sql_commands import run_sqlcmd
from app01.tasks.dvs_sc_page_analysis import get_testcase_result
from app01.utils.functions import download, start_triage_uuid,update_uuid_status,update_log_status
from app01.utils.functions import start_triage_file
from django.conf import settings
uuid_triage_path="uuid_triage"
file_triage_path="file_triage"
def log_test_add(request):
    tool_path = file_triage_path
    print("tool_path",tool_path)
    log_path = request.POST.get("log_path")
    filename=os.path.basename(log_path)
    gpu_name = "GPU"
    testsuite = "Testsuite"
    version = "Version"
    if request.POST.get("gpu"):
        gpu_name = request.POST.get("gpu")
    if request.POST.get("testsuite"):
        testsuite = request.POST.get("testsuite")
    if request.POST.get("version"):
        version = request.POST.get("version")
    log_pattern=gpu_name +"_"+ version +"_"+ testsuite
    print(log_pattern)
    download(log_path,os.path.join(tool_path,log_pattern+"_"+filename))
    start_triage_file(tool_path, log_pattern+"_"+filename, gpu_name, version, testsuite)
    models.log_triage.objects.create(log_link=log_path, status="Running", log_result="#"+log_pattern+"#")

def file_test_add(request):
    tool_path = file_triage_path
    file_object = request.FILES.get("logfile")
    filename=file_object.name
    print("filename",filename)
    gpu_name = "GPU"
    testsuite = "Testsuite"
    version = "Version"
    if request.POST.get("gpu"):
        gpu_name = request.POST.get("gpu")
    if request.POST.get("testsuite"):
        testsuite = request.POST.get("testsuite")
    if request.POST.get("version"):
        version=request.POST.get("version")
    log_pattern=gpu_name +"_"+ version +"_"+ testsuite
    f = open(os.path.join(tool_path,log_pattern+"_"+filename), mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    start_triage_file(tool_path,log_pattern+"_"+filename,gpu_name,version,testsuite)
    models.log_triage.objects.create(log_link=filename, status="Running", log_result="#" + log_pattern + "#")


def result_list(request):
    uuid_queryset = models.UUID_triage.objects.all()
    logresult_queryset=models.log_triage.objects.all()
    if request.method == "GET":
        uuid_running_tasks=models.UUID_triage.objects.filter(status="Running")
        for task in uuid_running_tasks:
            print("RRRR",task.UUID)
            update_uuid_status(task.UUID)

        log_running_tasts=models.log_triage.objects.filter(status="Running")
        for task in log_running_tasts:
            print("RRRR",task.log_result)
            update_log_status(task.log_result)
        uuid_queryset = models.UUID_triage.objects.all()

        logresult_queryset = models.log_triage.objects.all()
        return render(request, "triage_tasks.html", {"uuid_queryset": uuid_queryset,"logresult_queryset":logresult_queryset})
    if request.method == "POST":
        if request.POST.get("SUUID"):
            uuid_test_add(request)
        if request.POST.get("log_path"):
            log_test_add(request)
        if request.FILES:
            file_test_add(request)


    return render(request, "triage_tasks.html", {"uuid_queryset": uuid_queryset,"logresult_queryset":logresult_queryset})

def uuid_test_add(request):
    test_UUID = request.POST.get("SUUID")
    print("UUID",test_UUID)
    tool_path=uuid_triage_path

    print("tool_path",tool_path)
    uuid_result=start_triage_uuid(request,tool_path, test_UUID)
    status="Running"
    models.UUID_triage.objects.create(UUID=test_UUID,status=status,result_excel="#")
    return render(request, "triage_tasks.html")


def uuidresult_delete(request,nid):
    models.UUID_triage.objects.filter(id=nid).delete()
    return redirect("/triage/tasks/")

def logresult_delete(request,nid):
    models.log_triage.objects.filter(id=nid).delete()
    return redirect("/triage/tasks/")

