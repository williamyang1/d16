import os
from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModeForm
from app01 import models
def city_list(request):
    queryset = models.City.objects.all()
    if request.method == "GET":
        return render(request, "city_list.html",{"queryset":queryset})

    return HttpResponse("...")


class UpModelForm(BootStrapModeForm):
    bootstrap_exclude_fields = ["img"]
    class Meta:
        model =models.City
        fields = "__all__"

def city_add(request):
    title="New City"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, "upload_form.html",{"form":form,"title":title})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        print("XXXX", form.cleaned_data)

        return redirect("/city/list/")
    return render(request, "upload_form.html", {"title": title, "form": form})



