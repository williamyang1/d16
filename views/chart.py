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
from django_pandas.io import read_frame
from app01.utils.functions import create_list

def chart_list(request):
    return render(request, "chart_list.html")

def chart_nvbugs(request):

    legend =[['New_Bugs'],['QA_Recommended_Blocker_Open_Bug'],['cuDNN_All_Opening_Bugs'],['cuDNN_Unscrubbed_Open_Bugs'],
             ['cuDNN_Regression_Open_Bugs'],['cuDNN_QA_filed_Open_Bugs'],['Unscrubbed_QA_bugs'],['cuDNN_Bugs_Closed_This_Week']]
    # x_axis=["yiyue","2yue","3yue","4yue","5yue","6yue"]
    # #dates=models.BugChartTable.objects.dates()



    series_list=[[{
                     "name": legend[0],
                    "type": 'line',
                        "stack": 'Total',
        "smooth": True,
        "lineStyle": {
            "width": 4,
            "color": "#48b"

        },

        "data": create_list((models.BugChartTable.objects.values_list("NewBugs"))),
                }],
        [{
             "name": 'QA_Recommended_Blocker_Open_Bug',
            "type": 'line',
            "stack": 'Total',
            "smooth": True,
            "lineStyle": {
                "width": 4,
                "color": "#48b"

            },
            "data": create_list((models.BugChartTable.objects.values_list("QA_Recommended_Blocker"))),
        }],
        [{
             "name": 'cuDNN_All_Opening_Bugs',
            "type": 'line',
            "stack": 'Total',
            "smooth": True,
            "lineStyle": {
                "width": 4,
                "color": "#48b"
            },
            "data": create_list((models.BugChartTable.objects.values_list("All_Opening"))),
        }],
        [{
            "name": 'cuDNN_Unscrubbed_Open_Bugs',
            "type": 'line',
            "stack": 'Total',
            "smooth": True,
            "lineStyle": {
                "width": 4,
                "color": "#48b"

            },
            "data": create_list((models.BugChartTable.objects.values_list("Unscrubbed_Open"))),
        }],
        [{
             "name": 'cuDNN_Regression_Open_Bugs',
            "type": 'line',
            "stack": 'Total',
            "smooth": True,
            "lineStyle": {
                "width": 4,
                "color": "#48b"

            },
            "data": create_list((models.BugChartTable.objects.values_list("Regression"))),
        }],
        [{
             "name": 'cuDNN_QA_filed_Open_Bugs',
            "type": 'line',
            "stack": 'Total',
            "smooth": True,
            "lineStyle": {
                "width": 4,
                "color": "#48b"

            },
            "data": create_list((models.BugChartTable.objects.values_list("QA_filed"))),
        }],
        [{
            "name": 'Unscrubbed_QA_bugs',
            "type": 'line',
            "stack": 'Total',
            "smooth": True,
            "lineStyle": {
                "width": 4,
                "color": "#48b"

            },
            "data": create_list((models.BugChartTable.objects.values_list("Unscrubbed_QA"))),
        }],
        [{
            "name": 'cuDNN_Bugs_Closed_This_Week',
            "type": 'line',
            "stack": 'Total',
            "smooth": True,
            "lineStyle": {
                "width": 4,
                "color": "#48b"

            },
            "data": create_list((models.BugChartTable.objects.values_list("Closed_This_Week"))),
        }]
                ]
    result ={"status": True,
             "data":{
                 "legend":legend,
                 "smooth": True,
                 "lineStyle": {
                     "width": 4,
                     "color": "#48b"

                 },
                 "x_axis":list(models.BugChartTable.objects.values_list("Date")),
                 "series_list":series_list
             }
             }

    return JsonResponse(result)


