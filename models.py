from django.db import models

# Create your models here.
class Department(models.Model):
    """department table"""
    id=models.BigAutoField(verbose_name="id",primary_key=True)
    title=models.CharField(verbose_name='department title',max_length=32)
    def __str__(self):
        return self.title
class Userinfo(models.Model):
    """user info"""
    name=models.CharField(verbose_name="name",max_length=16)
    password=models.CharField(verbose_name="pwd",max_length=64)
    age=models.IntegerField(verbose_name="age")
    account=models.DecimalField(verbose_name="account left",max_digits=10, decimal_places=2,default=0)
    date_time=models.DateField(verbose_name='Time')

    depart=models.ForeignKey(verbose_name="Depart Name",to="Department",on_delete=models.CASCADE, to_field="id")
    #depart = models.ForeignKey(to="Department", to_fields="title",null=True,blank=True, on_delete=models.SET_NULL)


    gender_choice=(
        (1,"male"),
        (2,"famale"),
    )
    gender =models.SmallIntegerField(verbose_name="gender",choices=gender_choice)

class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name="telephone number", max_length=11)
    price = models.IntegerField(verbose_name="price", default=0, null=True, blank=True)
    level_choice=(
        (1,"one level"),
        (2,"two level"),
        (3,"three level"),
    )
    level = models.SmallIntegerField(verbose_name="level",choices=level_choice,default=1)
    status_choice = (
        (1, "used"),
        (2, "not used"),
    )
    status = models.SmallIntegerField(verbose_name="status",choices=status_choice,default=2)

class Admin(models.Model):
    username=models.CharField(verbose_name="user name", max_length=32)
    password=models.CharField(verbose_name="pwd",max_length=64)
    def __str__(self):
        return self.username
class Task(models.Model):
    level_choices=(
        (1,"urgent"),(2,"imponent"),(3,"temporary")
    )
    level =models.SmallIntegerField(verbose_name="level",choices=level_choices,default=1)
    title= models.CharField(verbose_name="title",max_length=64)
    detail=models.TextField(verbose_name="detail")
    user= models.ForeignKey(verbose_name="responsible user",to="Admin",to_field="id",on_delete=models.CASCADE)

class Order(models.Model):
    oid=models.CharField(verbose_name="order",max_length=32)
    title=models.CharField(verbose_name="title",max_length=32)
    price=models.IntegerField(verbose_name="price")
    status_choices=((1,"payed"),(2,"Not pay"))
    status = models.SmallIntegerField(verbose_name="status",choices=status_choices,default=1)
    admin=models.ForeignKey(verbose_name="admin",to=Admin,to_field="id", on_delete=models.CASCADE)

class Boss(models.Model):
    name =models.CharField(verbose_name="name",max_length=32)
    age = models.IntegerField(verbose_name="age")
    img = models.CharField("head",max_length=64)

class City(models.Model):
    name =models.CharField(verbose_name="city",max_length=32)
    count = models.IntegerField(verbose_name="person")
    img = models.FileField("logo",max_length=128,upload_to="city/")


class NvBug(models.Model):
    BugId=models.IntegerField(verbose_name="BugID")
    Synopsis=models.CharField(verbose_name="Synopsis",max_length=200)
    BugAction=models.CharField(verbose_name="BugAction",max_length=100)
    Module=models.CharField(verbose_name="Module",max_length=100)
    Priority=models.CharField(verbose_name="Priority",max_length=100)
    RequestDate = models.DateField(verbose_name="RequestDate")
    Categories = models.CharField(verbose_name="Categories", max_length=100 ,null=True, blank=True)
    Disposition = models.CharField(verbose_name="Disposition", max_length=100)
    QAEngineer = models.CharField(verbose_name="QAEngineer", max_length=100)
    Engineer = models.CharField(verbose_name="Engineer", max_length=200 ,null=True, blank=True)
    CustomKeywords = models.CharField(verbose_name="CustomKeywords", max_length=200 ,null=True, blank=True)
    ModifiedDate = models.DateTimeField(verbose_name="ModifiedDate")
    Version = models.CharField(verbose_name="Version", max_length=100 ,null=True, blank=True)
    Origin = models.CharField(verbose_name="Origin", max_length=100)
    Regression = models.CharField(verbose_name="Regression", max_length=50,null=True, blank=True)
    Error = models.TextField(verbose_name="Error" )
    Tlist = models.TextField(verbose_name="Tlist")
    buglink = models.CharField(verbose_name="buglink", max_length=200)
    DaysOpen = models.IntegerField(verbose_name="DaysOpen",default=0)


class BugChartTable(models.Model):
    Date= models.CharField(verbose_name="Date",max_length=50)
    NewBugs=models.SmallIntegerField(verbose_name="NewBugs")
    QA_Recommended_Blocker=models.SmallIntegerField(verbose_name="QA_Recommended_Blocker_Open_Bug")
    All_Opening = models.SmallIntegerField(verbose_name="cuDNN_All_Opening_Bugs")
    Unscrubbed_Open = models.SmallIntegerField(verbose_name="cuDNN_Unscrubbed_Open_Bugs")
    Regression = models.SmallIntegerField(verbose_name="cuDNN_Regression_Open_Bugs")
    QA_filed = models.SmallIntegerField(verbose_name="cuDNN_QA_filed_Open_Bugs")
    Unscrubbed_QA = models.SmallIntegerField(verbose_name="Unscrubbed_QA_bugs")
    Closed_This_Week = models.SmallIntegerField(verbose_name="cuDNN_Bugs_Closed_This_Week")

class UUID(models.Model):
    UUID =models.CharField(verbose_name="UUID",max_length=32)
    CL = models.CharField(verbose_name="cl",max_length=32)
    version = models.CharField(verbose_name="version",max_length=32)


