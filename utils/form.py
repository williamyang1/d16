from app01.utils.bootstrap import BootStrapModeForm
from django import forms
from app01 import models
from django.core.validators import RegexValidator, ValidationError

class UserModeForm(BootStrapModeForm):
    name=forms.CharField(min_length=3, label="user name")
    #password = forms.CharField(min_length=3, label="user name")
    class Meta:
        model=models.Userinfo
        fields = ["name", "password", "age","account","date_time","gender","depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

class PrettyForm(BootStrapModeForm):
    mobile =forms.CharField(
        label="telephone number",
        validators = [RegexValidator(r'^137[0-9]+$', "number must start with 137")]
                     # RegexValidator(r'^/d{10}$', "phone number format error")]
                            )
    class Meta:
        model=models.PrettyNum
        fields = "__all__"


    def clean_mobile(self):
        txt_mobile =self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("the phone number have exist!")
        if len(txt_mobile) != 11:
            raise ValidationError("format error")
        return txt_mobile

class PrettyEditForm(BootStrapModeForm):
    mobile=forms.CharField(disabled=True,label="phone number")
    class Meta:
        model=models.PrettyNum
        fields = ["mobile","price","level","status"]


    def clean_mobile(self):
        self.instance.pk
        txt_mobile =self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("the phone number have exist!")
        if len(txt_mobile) != 11:
            raise ValidationError("format error")
        return txt_mobile