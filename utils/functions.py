import subprocess
import os
def create_list(queryset):
    value=[]
    for i in queryset:

        value.append(i[0])
    return value

def nvidia_login(url):
    import requests
    from requests.auth import HTTPBasicAuth

    r = requests.get(url=url, auth=HTTPBasicAuth("williamy", "Williamy1203#"))
    print(r.text)

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    return out, err, p.returncode

def download(src,dest):
    cmd = "axel -n 100 "+ str(src) +"  --quiet --output " +str(dest)
    filename=os.path.basename(src)
    print(filename)
    os.system(cmd)

    if os.path.exists(dest):
        print("Download pass")
    else:
        print("Download filed")
    return os.path.join(dest,filename)

def log_file_triage(tool_path,logfile,gpu,testsutie):
    cmd="python3 " + os.path.join(tool_path,"triage_log_file.py") +" --logfile " + logfile + " --gpu " + gpu + " --suite " +testsutie
    print(cmd)
    out, err, returncode=run_cmd(cmd)
    print("OOOout",out)
    return out

def triage_uuid(tool_path, uuid):
    cmd="python3 " + os.path.join(tool_path,"main.py") +" --uuid " + str(uuid)
    print(cmd)
    #out, err, returncode=run_cmd(cmd)
    # print("##########",out)
    excel_folder=os.path.join(tool_path,"data","result")
    #tmp=os.system("ls -lt " + excel_folder)
    tmp = """total 112
    -rw-rw-r-- 1 williamy williamy 26112 9月  28 17:57 dvs_sc_31801822_test_result__2022-09-28-15:51:51:0dag.xls
    -rw-rw-r-- 1 williamy williamy 26112 9月  28 17:57 aa.xls
    -rw-rw-r-- 1 williamy williamy 26112 9月  28 17:57 dvs_sc_31801822_test_result__2022-09-28-15:51:51:0dag.xls
    -rw-rw-r-- 1 williamy williamy 26112 9月  28 15:51 dvs_sc_31801822_test_result__2022-09-28-15:51:51:09S.xls
    """
    excel_name=get_excel(tmp)
    return excel_name

def get_excel(out):
    excel_n=out.split("\n")[1].split(" ")[-1]
    print(excel_n)
    return excel_n
