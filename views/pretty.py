from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator, ValidationError
from django.utils.safestring import mark_safe
from app01.utils.pageaction import PageInaction
from app01.utils.bootstrap import BootStrapModeForm
from app01.utils.form import *

def pretty_list(request):
    #page=int(request.GET.get("page",1))
    data_dict = {}
    search_data=request.GET.get('q',"")
    if search_data:
        data_dict["mobile__contains"]=search_data
    queryset=models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = PageInaction(request, queryset)
    page_queryset=page_object.page_queryset
    page_str=page_object.html()
    content={"queryset":page_queryset,
             "search_data":search_data,
             "page_string":page_str}
    return render(request,"pretty_list.html",content)



def pretty_add(request):

    if request.method == "GET":
        form =PrettyForm()
        return render(request,"pretty_add.html", {"form":form})
    form=PrettyForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    else:
        print(form.errors)
        return render(request,"pretty_add.html", {"form":form})



def pretty_edit(request,nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditForm(instance=row_object)
        #row_data = models.Department.objects.filter(id=nid).first()
        return render(request,"pretty_edit.html",{"form":form})

    form=PrettyEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request,"pretty_edit.html",{"form":form})

def pretty_delete(request,nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")
