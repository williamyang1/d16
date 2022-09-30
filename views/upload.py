import os
from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModeForm
from app01 import models
def upload_list(request):
    if request.method == "GET":
        return render(request, "upload_list.html")
    print(request.POST)
    print(request.FILES)
    file_object=request.FILES.get("avatar")
    print(file_object.name)
    f = open(file_object.name,mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse("...")

class UpForm(BootStrapForm):
    bootstrap_exclude_fields=["img"]
    name =forms.CharField(label="name")
    age =forms.IntegerField(label="age")
    img =forms.FileField(label="head")

def upload_form(request):
    from django.conf import settings
    title="Form upload"
    if request.method == "GET":
        form=UpForm()

        return render(request, "upload_form.html",{"title":title,"form":form})

    form =UpForm(data=request.POST,files=request.FILES)
    if form.is_valid():

        print("XXXX",form.cleaned_data)
        print(form.cleaned_data.get("img"))
        image_object=form.cleaned_data.get("img")

        media_path=os.path.join(settings.MEDIA_ROOT,image_object.name)
        print(media_path)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age = form.cleaned_data["age"],
            img = media_path,
        )
        return HttpResponse("...")
    return render(request, "upload_form.html",{"title":title,"form":form})

class UpModelForm(BootStrapModeForm):
    bootstrap_exclude_fields = ["img"]
    class Meta:
        model =models.City
        fields = "__all__"

def upload_modalform(request):
    title="model upload"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, "upload_form.html",{"form":form,"title":title})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        print("XXXX", form.cleaned_data)

        return HttpResponse("success")
    return render(request, "upload_form.html", {"title": title, "form": form})