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
from app01.utils.functions import download, log_file_triage, triage_uuid



def triage_tasks(request):
    result_dict = {
        "name": None,
        "result_link":None,
        "gpu":"None",
        "testsuite":"None",
        "download":None
    }

    if request.method == "GET":
        return render(request, "triage_tasks.html", {"result_dict":result_dict})
    print(request.POST)

    if request.POST.get("SUUID"):
        test_UUID = request.POST.get("SUUID")
        print("UUID",test_UUID)
        tool_path="uuid_triage"
        uuid_result=triage_uuid(tool_path, test_UUID)
        result_dict["name"] = "Download test result excel"
        result_dict["download"] = uuid_result
        cmd1 = "mv " + uuid_result + " media"
        # os.system(cmd1)
        return render(request, "triage_tasks.html", {"result_dict": result_dict})

    if request.POST.get("log_path"):
        log_path=request.POST.get("log_path")
        filename=os.path.basename(log_path)
        download(log_path,os.path.join("media",filename))

    if request.FILES:
        file_object = request.FILES.get("logfile")

        filename=file_object.name
        f = open(os.path.join("media",file_object.name), mode='wb')
        for chunk in file_object.chunks():
            f.write(chunk)
        f.close()
    if request.POST.get("gpu"):
        result_dict["gpu"]=request.POST.get("gpu")
    if request.POST.get("testsuite"):
        result_dict["testsuite"]=request.POST.get("testsuite")

    tool_path="log_triage"
    log=os.path.join("media",filename)
    out=log_file_triage(tool_path,log,result_dict["gpu"],result_dict["testsuite"])
    out="""./v100_version_cudnn_level_tests_L3_2022-09-28-06-52-14-09S.html
    ==> [error msg]   @@@@ errmsg  : CUDNN error at fusedConvBackendTest.cpp:945, code=6 (CUDNN_STATUS_ARCH_MISMATCH) in 'status'
    ==> items below:
    &&&& FAILED cudnnTest -dimA5,56,45,81 -filtA40,56,3,3 -padA1,1 -RbnActConvBackend -fusedScale0 -fusedBias0 -fusedActivation0 -fusedStats1 -Pinh -Pouth -P
    comps -formatAll1 -x -dim2 -knobTileOpt="""
    triage_result_link=out.split("\n")[0].strip().strip("./")

    cmd1="mv " + triage_result_link + " media"
    #os.system(cmd1)
    result_dict["name"]=triage_result_link
    result_dict["result_link"] = triage_result_link
    return render(request, "triage_tasks.html", {"result_dict":result_dict})




def triage_regression(request):

    title="check regression"
    # configuration = "cudnn_rc_hopper_cuda_11.8 Release rocky8-64 ci7qc tu104_pg180_0500 DX0 CUDNN.NEGATIVE.TESTS"
    # UUID = "3181406839432407.0"
    # testCase = "mnist"
    result_list = []
    if request.method == "GET":
        return render(request, "regression_check.html",{"result_list":result_list})
    # if request.method == "GET":
    print(request.POST)
    #UUID=request.POST.get("UUID")
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

    content_list=[]
    for version in version_list:

        UUID=models.UUID.objects.filter(version=version).first().UUID

        result=get_testcase_result(str(UUID),str(configuration),str(testCase))

        content_list.append({
        "configuration" : configuration,
        "version" : version,
        "testCase" : testCase,
        "result":result
        })
    output_list=[]
    if request.POST.get("commands"):
        cmd = request.POST.get("commands")
        print(cmd)
        output_list = run_sqlcmd(cmd)
        print(output_list)
    return render(request, "regression_check.html",{"content_list":content_list,"result_list":output_list})
