from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator, ValidationError
from django.utils.safestring import mark_safe

from app01.utils.pageaction import PageInaction
from app01.utils.bootstrap import BootStrapModeForm
from app01.utils.form import *
from app01.utils.encrypt import md5

def admin_list(request):
    info_dict=request.session["info"]
    print(info_dict)
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)
    page_obj = PageInaction(request, queryset, page_size=10)
    context = {
        "queryset":page_obj.page_queryset,
        "page_string":page_obj.html(),
        "search_data":search_data
   }
    return render(request, "admin_list.html", context)


class AdminForm(BootStrapModeForm):
    confirm_password=forms.CharField(
        label="confirm password",
        widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.Admin
        fields =["username", "password","confirm_password"]
        widgets={
            "password":forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        print(self.cleaned_data)
        confirm = md5(self.cleaned_data.get("confirm_password"))
        pwd=self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("password not same, please re-input")
        return confirm


class AdminEditForm(BootStrapModeForm):

    class Meta:
        model = models.Admin
        fields =["username"]




def admin_add(request):
    title= "New Amdin"
    if request.method == "GET":
        form = AdminForm()
        return render(request,"change.html", {"form":form,"title":title})

    form=AdminForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect("/admin/list/")
    else:
        print(form.errors)
        return render(request,"change.html", {"form":form,"title":title})

def admin_edit(request,nid):
    title= "edit Amdin"
    row_object = models.Admin.objects.filter(id=nid).first()
    print("row_object",row_object)
    if not row_object:
        return render(request,"error.html",{"msg":"Data is not exist!!!$$$"})
    if request.method == "GET":
        form = AdminForm(instance=row_object)
        return render(request,"change.html", {"form":form,"title":title})

    form=AdminForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request,"change.html", {"form":form,"title":title})

def admin_delete(request,nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")

class AdminResetModeForm(BootStrapModeForm):
    confirm_password = forms.CharField(
        label="confirm password",
        widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.Admin
        fields = ["password","confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        md5_pwd=md5(pwd)
        exist=models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exist:
            raise ValidationError("password can't same as previous!")
        return md5(pwd)

    def clean_confirm_password(self):
        print(self.cleaned_data)
        confirm = md5(self.cleaned_data.get("confirm_password"))
        pwd=self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("password not same, please re-input")
        return confirm

def admin_reset(request,nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    title= "Reset Amdin - {}".format(row_object.username)
    print("row_object",row_object)
    if not row_object:
        return render(request,"error.html",{"msg":"Data is not exist!!!$$$"})
    if request.method == "GET":
        form=AdminResetModeForm()
        render(request, "change.html", {"form": form, "title": title})
    form = AdminResetModeForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request,"change.html", {"form":form,"title":title})