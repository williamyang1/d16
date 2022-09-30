from django.shortcuts import render, redirect,HttpResponse
from app01 import models
from django import forms
from django.core.validators import RegexValidator, ValidationError
from django.utils.safestring import mark_safe
from app01.utils.pageaction import PageInaction
from app01.utils.bootstrap import BootStrapModeForm
from app01.utils.form import *

def user_list(request):
    queryset=models.Userinfo.objects.all()
    page_obj=PageInaction(request,queryset,page_size=10)
    context={
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html()
    }
    for obj in queryset:
        print(obj.name,obj.name,obj.depart.title,obj.get_gender_display(),obj.account, obj.date_time.strftime("%Y-%m-%d"))
    return render(request,"user_list.html",context)


def user_modeform_add(request):
    if request.method == "GET":
        form =UserModeForm()
        return render(request,"user_mode_form_add.html", {"form":form})
    form=UserModeForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect("/user/list/")
    else:
        print(form.errors)
        return render(request,"user_mode_form_add.html", {"form":form})

def user_add(request):
    queryset=models.Department.objects.all()
    context={
        "gender_choices":models.Userinfo.gender_choice,
        "depart_list":models.Department.objects.all()
    }
    if request.method == "GET":
        return render(request,"user_add.html",context)
    user=request.POST.get("name")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    account = request.POST.get("account")
    ctime = request.POST.get("intime")
    gender = request.POST.get("gd")
    depart_id = request.POST.get("dp")

    models.Userinfo.objects.create(name=user,password=pwd,age=age,
                                   account=account,date_time=ctime,
                                   gender=gender,
                                   depart_id=depart_id)
    return redirect("/user/list/")
def user_delete(request,nid):
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")

def user_edit(request,nid):
    row_object = models.Userinfo.objects.filter(id=nid).first()
    form = UserModeForm(instance=row_object)
    if request.method == "GET":
        #row_data = models.Department.objects.filter(id=nid).first()
        return render(request,"user_edit.html",{"form":form})

    form=UserModeForm(data=request.POST, instance=row_object)
    if form.is_valid():
        #form.instance.Xname=value
        form.save()
        return redirect("/user/list/")
    return render(request,"user_edit.html",{"form":form})