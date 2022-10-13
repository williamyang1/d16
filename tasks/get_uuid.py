from bs4 import BeautifulSoup
import requests
url="http://scdvsweb.nvidia.com/DVSWeb/view/content/changelist/buildChangelists.jsf?submitter=Jason%20Reid&branch=cudnn_rc_hopper_cuda_11.8&mode=Automatic"
def getPage(url):
    try:
        res=requests.get(url=url)

        return res.text
    except Exception:
        print("The page can't be opened")

def get_version_list(branch):

    urlb="http://scdvsweb.nvidia.com/DVSWeb/view/content/changelist/buildChangelists.jsf?submitter=GA - Jason Reid&branch="+ branch+"&mode=Automatic"
    result_list=[]
    html_txt = login_get_page(urlb)
    soup = BeautifulSoup(html_txt, 'html.parser')

    table_node = soup.find_all('table')[-1]
    lines = table_node.findAll('tr')
    for line in lines[2:]:
        uuid,cl,version=content_analysis(line)
        # print("UUUUUUUUU",uuid,cl,version)
        result_list.append((uuid,cl,version))
    return result_list
def content_analysis(line):

    uuid=line.find_all("a")[0].get("href").split("=")[-1].strip()
    cl=line.find_all("a")[0].get_text().split(".")[0].strip()
    version=line.find_all("td")[0].get_text().split(":")[0].split(".")[-1]
    return uuid,cl,version

def login_get_page(url):
    from requests.auth import HTTPBasicAuth

    try:
        r = requests.get(url=url,auth=HTTPBasicAuth("williamy","Y20hg1203wi45#"))
        #print(r.text)
        return r.text
    except Exception:
        print("The page can't be opened")

if __name__ == '__main__':
    get_version_list("cudnn_rc_hopper_cuda_11.8")

    # html_txt=login_get_page(url)
    # # html_txt=getPage(url)
    # # print(html_txt)
    # content_analysis(html_txt)