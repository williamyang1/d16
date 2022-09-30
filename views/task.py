import json
from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from app01.utils.bootstrap import BootStrapModeForm
from app01 import models
from app01.utils.pageaction import PageInaction
class TaskModeForm(BootStrapModeForm):
    class Meta:
        model = models.Task
        fields= "__all__"
        widgets ={
            #"detail": forms.Textarea,
            "detail": forms.TextInput
        }

def task_list(request):
    form=TaskModeForm()
    queryset=models.Task.objects.all().order_by("-id")
    page_object=PageInaction(request,queryset,page_size=5)
    content={
        "form":form,
        "queryset":page_object.page_queryset,
        "page_string":page_object.html()
    }
    return render(request, "task_list.html",content)

@csrf_exempt
def task_ajax(request):
    data_dict={
        "status":True,
        "data":[11,22,33]
    }
    json_string=json.dumps(data_dict)
    return HttpResponse(json_string)

@csrf_exempt
def task_add(request):
    print(request.POST)
    form =TaskModeForm(data =request.POST)
    if form.is_valid():
        form.save()
        data_dict={ "status":True }
        return HttpResponse(json.dumps(data_dict))
    data_dict={"status": False,'error':form.errors}
    return HttpResponse(json.dumps(data_dict))