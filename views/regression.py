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
from django.conf import settings

def regression(request):
    title="check regression"
    output_list = []
    content_list = []
    if request.method == "GET":
        return render(request, "regression_check.html")

    print(request.POST)
    if request.POST.get("commands"):
        cmd = request.POST.get("commands")
        print(cmd)
        output_list = run_sqlcmd(cmd)
        print(output_list)

    if request.POST.get("version"):
        version = request.POST.get("version")
        testCase = request.POST.get("testcase")
        configuration = request.POST.get("configuration")
        version_list=[version]
        version_last=version.split(".")[-1]
        version_list.append(".".join(version.split(".")[:-1])+ "." + str((int(version_last) - 1)) )
        version_list.append(".".join(version.split(".")[:-1])+ "." + str((int(version_last) - 2)) )
        version_list.append(".".join(version.split(".")[:-1])+ "." + str((int(version_last) - 3)) )
        version_list.append(".".join(version.split(".")[:-1])+ "." + str((int(version_last) - 4)) )
        version_list.append(".".join(version.split(".")[:-1])+ "." + str((int(version_last) - 5)) )
        print("VVVVVVVVVVVV",version_last)

        for version in version_list:
            UUID=models.UUID.objects.filter(version=version).first().UUID
            result=get_testcase_result(str(UUID),str(configuration),str(testCase))
            content_list.append({
            "configuration" : configuration,
            "version" : version,
            "testCase" : testCase,
            "result":result
            })
    return render(request, "regression_check.html",{"content_list":content_list,"result_list":output_list})
