import re
import json
import requests
cudnn_new_bugs=200040955
cuDNN_QA_filed_open_Bugs=200045751
QA_actionable_buts=200053667
class NvbugsUtils:
    def __init__(self,user,password):
        self.user = user
        self.password = password
    def get_bug_details(self,bugid):
        url="https://nvbugsapi.nvidia.com/nvbugswebserviceapi/api/bug/getbug/"+str(bugid)
        #print(self.user)
        try:
            r=requests.get(url,auth=(self.user, self.password))
            print(r.json())

            content = r.json()
            #print(content["ReturnValue"]["DescriptionPlainTextReadOnly"])
            BugId=content["ReturnValue"]["BugId"]
            Synopsis=content["ReturnValue"]["Synopsis"]
            BugAction=content["ReturnValue"]["BugAction"]["Value"]
            Engineer=content["ReturnValue"]["Engineer"]["Value"]
            Version=content["ReturnValue"]["Version"]
            Module=content["ReturnValue"]["ModuleInfo"]["Value"]
            Disposition=content["ReturnValue"]["Disposition"]["Value"]
            Regression=content["ReturnValue"]["Regression"]
            Keywords=content["ReturnValue"]["CustomKeywords"]
            Created=content["ReturnValue"]["RequestDate"].split("T")[0]
            DaysOpen=content["ReturnValue"]["DaysOpen"]
            Origin=content["ReturnValue"]["Origin"]
            Version=content["ReturnValue"]["Version"]
            ModifiedDate=content["ReturnValue"]["ModifiedDate"].split("T")[0]

            Priority=content["ReturnValue"]["Priority"]["Value"]
            RequestDate=content["ReturnValue"]["RequestDate"].split("T")[0]
            Categories=content["ReturnValue"]["Categories"]

            QAEngineer=content["ReturnValue"]["QAEngineer"]["Value"]
            return(BugId,Synopsis,BugAction,Engineer,Version,Module,Disposition, Regression,Keywords,Created,DaysOpen,Origin,Version, ModifiedDate,Priority,RequestDate,Categories,QAEngineer)
        except Exception as e:
            print(e)
    def get_bug_list(self,):
        url="https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Search/GetBugs?page=1&limit=10"
        request_body=[
            {"FieldName":"BugEngineerFullName","FieldValue":""},
            {"FieldName":"BugRequesterFullName","FieldValue":""},
            {"FieldName":"QAEngineerFullName","FieldValue":""}
           ]
        r = requests.post(url,auth=(self.user, self.password),json=request_body)
        print(r.json())
    def get_keyword(self):
        #https://confluence.nvidia.com/display/NVBUG/GetKeyword
        url="https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Keyword/Get"
        request_body = {"AppDivisionID": "1",
             "KeywordNames": ["cuDNN 8.2.1"]}
        r = requests.post(url, auth=(self.user, self.password), json=request_body)
        print(r.json())
    def get_watchlist(self,watchlistid):
        #https: // confluence.nvidia.com / display / NVBUG / GetSavedSearchBugs
        url="https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Search/GetSavedSearchBugs?id="+str(watchlistid)
        r=requests.get(url,auth=(self.user, self.password))
        #print(r.json())
        buglist=[]
        content = r.json()
        for i in content["ReturnValue"]:
            print(i['BugId'])
            buglist.append(i['BugId'])
        return buglist

def get_buglist_detail():
    bug = NvbugsUtils("williamy", "Abcd2345")
    # print(bug.get_bug_details(200742297))
    # bug.get_bug_list()
    buglist = bug.get_watchlist(cudnn_new_bugs)
    results = []
    for bugid in buglist:
        results.append(bug.get_bug_details(bugid))
    print("Done")
    return results


def main():
    bug=NvbugsUtils("williamy","Williamy1203#")
    print(bug.get_bug_details(200742297))
    bug.get_bug_list()
    # buglist=bug.get_watchlist(cudnn_new_bugs)
    buglist = bug.get_watchlist(QA_actionable_buts)
    results=[]
    for bugid in buglist:
        results.append(bug.get_bug_details(bugid))
    print("Done")
    print(results)

if __name__ == "__main__":
    main()



