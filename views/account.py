from django.shortcuts import render, redirect,HttpResponse
from app01 import models
from django import forms
from django.core.validators import RegexValidator, ValidationError
from django.utils.safestring import mark_safe

from app01.utils.pageaction import PageInaction
from app01.utils.bootstrap import BootStrapModeForm
from app01.utils.form import *
from app01.utils.encrypt import md5
class loginform(forms.Form):
    username=forms.CharField(
        label="user name",
        widget=forms.TextInput(attrs={"class":"form-control"}),
        required=True
    )
    password=forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={"class":"form-control"}),
        required=True
    )
    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        return md5(pwd)
def login(request):
    if request.method == "GET":
        form=loginform()
        return render(request, "login.html",{"form":form})
    form=loginform(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password","user or password error")
            return render(request, "login.html", {"form": form})
        request.session["info"] = {"id":admin_object.id, "name":admin_object.username}
        return redirect("/admin/list/")

    return render(request, "login.html",{"form":form})

def logout(request):
    request.session.clear()
    return redirect("/login/")

