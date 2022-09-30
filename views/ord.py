import json
import random
from datetime import datetime
from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from app01.utils.bootstrap import BootStrapModeForm
from app01 import models
from app01.utils.pageaction import PageInaction

class OrderModelForm(BootStrapModeForm):
    class Meta:
        model=models.Order
        #fields = "__all__"
        exclude=["oid","admin"]


def ord_list(request):
    form = OrderModelForm()
    queryset = models.Order.objects.all().order_by("-id")
    page_object = PageInaction(request, queryset)
    content = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, "ord_list.html", content)

def ord_delete(request):
    uid=request.GET.get("uid")
    exists =models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status":False, "error":"Delete failed, Data is not exist"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status":True})


@csrf_exempt
def ord_add(request):
    print("AAAAAAAAAAA")
    form=OrderModelForm(data=request.POST)
    print(request.POST)

    if form.is_valid():
        form.instance.oid=datetime.now().strftime("%Y%m%d%H%M%S") +str(random.randint(10,99))
        form.instance.admin_id =request.session["info"]["id"]
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    data_dict = {"status": False, 'error': form.errors}
    return JsonResponse(data_dict)


def ord_detail(request):
    uid=request.GET.get("uid")
    row_dict =models.Order.objects.filter(id=uid).values("title","price","status").first()
    print("DDDDDD")
    if not row_dict:
        return JsonResponse({"status":False, "error":"Data is not exist"})
    result= {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)

@csrf_exempt
def ord_edit(request):
    uid=request.GET.get("uid")

    row_object=models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "Data is not exist"})
    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})