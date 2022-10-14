import subprocess
import os
from subprocess import Popen
from app01 import models
import shlex
def create_list(queryset):
    value=[]
    for i in queryset:
        value.append(i[0])
    return value

def nvidia_login(url):
    import requests
    from requests.auth import HTTPBasicAuth
    r = requests.get(url=url, auth=HTTPBasicAuth("williamy", "Y20hg1203wi45#"))
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
    print(cmd)
    if os.path.exists(dest):
        print("Download pass")
    else:
        print("Download filed")
    return os.path.join(dest,filename)

def start_triage_file(tool_path,log_filename,gpu_name,version,testsuite):
    cmd="cd  "+ tool_path+ "&& python3 triage_log_file.py --logfile " + log_filename + " --gpu " + gpu_name + " --suite " +testsuite + " --cudnnVersion " +version
    print(cmd)
    proc = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.pid:
        out="Cmd start"
        print()
    else:
        out="###Cmd can't start###"
    print(out)
    return out

def start_triage_uuid(tool_path, uuid):
    filetmp="tmp.txt"
    outfile = open(filetmp, "a+")
    cmd="cd "+tool_path +"&& python3  main.py --uuid " + str(uuid)
    print(cmd)
    proc = Popen(shlex.split(cmd), shell=True, stdout=outfile)
    if proc.pid:
        out = "Cmd start"
        
        print(proc.pid)
    else:
        out = "###Cmd can't start###"
    print(out)
    return out


def update_uuid_status(uuid):
    cl=uuid.split(".")[0].strip()
    cmd = 'ls uuid_triage/data/result/ | grep "dvs_sc_' + str(cl) + '" >tmp.txt'
    out = os.system(cmd)
    file_name="dvs_sc_"+str(cl)+'.xls'
    with open("tmp.txt") as f:
        outtext = f.readline()
        print("outtext", outtext)
    if outtext.find(cl) != -1:
        cmd1 = "cd uuid_triage/data/result/ && mv " + outtext.strip() + " " + file_name
        cmd2 = "cd uuid_triage/data/result/ && mv " + file_name + " " + "../../../media/uuid_result"
        print(cmd1)
        print(cmd2)
        os.system(cmd1)
        os.system(cmd2)
        if os.path.exists("media/uuid_result/" + file_name):
            print("File exist")
            models.UUID_triage.objects.filter(UUID=uuid).update(status="Completed", result_excel="uuid_result/"+file_name)
        else:
            print("File in not exist")
    else:
        print("No test result for this uuid")


def update_log_status(log_pattern):
    output_pattern = log_pattern.strip("#")
    print(output_pattern)
    cmd = 'ls file_triage/dlqa_triage/ | grep  ' + output_pattern + '| grep ".html" >tmp.txt'
    out = os.system(cmd)
    with open("tmp.txt") as f:
        outtext = f.readline()
        print("outtext", outtext)
        file_name=outtext.strip()
    if outtext.find(output_pattern) != -1:
        # cmd1 = "cd uuid_triage/data/result/ && mv " + outtext.strip() + " " + file_name
        cmd2 = "cd file_triage/dlqa_triage/ && mv " + file_name + " ../../media/log_result/"
        print("CMD",cmd2)
        print("###")
        os.system(cmd2)
        if os.path.exists("media/log_result/" + file_name):
            print("File exist")
            models.log_triage.objects.filter(log_result =log_pattern).update(status="Completed",
                                                                log_result="log_result/" + file_name)
        else:
            print("File in not exist")
    else:
        print("No test result for this log file")

