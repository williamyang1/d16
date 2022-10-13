from bs4 import BeautifulSoup
import urllib3
import requests
#test_result="https://scvrlweb.nvidia.com/showjob.php?job=9438406"
test_result="..."
#uuid_link="http://scdvs.nvidia.com/Regression_Results?which_changelist=3180904939432407.2&which_page=current_regressions&which_category=Extended+Sanity"
uuid_link="http://scdvs.nvidia.com/Regression_Results?which_changelist=3181850739432407.0&which_page=current_regressions&which_category=Extended+Sanity"

def getPage(url):
    try:
        res=requests.get(url=url)
        return res.text
    except Exception:
        print("The page can't be opened")

def content_analysis(page_text):
    soup = BeautifulSoup(page_text,'html.parser')
    title_node=soup.find("title")
    # print(title_node.get_text())
#    print(soup.get_text())

    for link in soup.find_all('a'):
        #print("LLLLLLLLLL",link.get('href'))
        pass

    table_node=soup.find_all('table')
    # print(len(table_node))
    myteble=table_node[1]
    result=[]

    for tr in myteble.findAll('tr'):

        result_line = []
        for td in tr.findAll("td"):
            #print(td.get_text())
            result_line.append(td.get_text())
        result.append(result_line)
    # print(myteble.get_text())

    start_time_Index=result[0].index("jobstarted PDT")
    end_time_Index=result[0].index("finished PDT")
    # print(result[1][start_time_Index])
    # print(result[1][end_time_Index])
    start=result[1][start_time_Index]
    end=result[1][end_time_Index]
    dateS=start.split()[0].split("-")[-1]

    # print(start.split()[1].split(":"))
    timeS=start.split()[1].split(":")
    dateE = end.split()[0].split("-")[-1]
    timeE = end.split()[1].split(":")
    durationTime=((int(dateE)-int(dateS))*24+int(timeE[0])-int(timeS[0]))*60+int(timeE[1])-int(timeS[1])
    print("durationTime:",durationTime)
    return int(durationTime)

def get_all_tests(page_text):
    #print(page_text)
    soup = BeautifulSoup(page_text,'html.parser')
    title_node=soup.find("title")
    print(title_node.get_text())
    #print("AAAAAAAA",soup.a)
    #print(soup.get_text())

    for link in soup.find_all('a'):
        #print("LLLLLLLLLL",link.get('href'))
        pass
    table_node=soup.find_all('table')
    print(len(table_node))
    test_result_table=table_node[13::3]
    results=[]
    print(len(test_result_table))
    result={}
    for mytable in test_result_table:
        print("NEW table")


        for tb in mytable.find_all('a'):
            link=tb.get('href')

            if link.find("job=") != -1:
                results.append(link)
    for i in results:
        print(i)

    return results


def get_specific_links(page_text):
    # print(page_text)
    soup = BeautifulSoup(page_text, 'html.parser')
    table_node = soup.find_all('table')

    test_result_table = table_node[13::3]


    result_dict = {}
    for mytable in test_result_table:
        for row in mytable.find_all("tr"):
            if len(row.find_all("td")) == 8:
                testsuite = row.find_all("td")[1].get_text()

            if len(row.find_all("td")) == 15:
                branch = row.find_all("td")[0].get_text()
                Type = row.find_all("td")[1].get_text()
                Platform = row.find_all("td")[2].get_text()
                if Platform.find(" ")!=-1:
                    Platform= "_".join(Platform.split(" "))

                CPU = row.find_all("td")[3].get_text()
                GPU = row.find_all("td")[4].get_text()
                DX = row.find_all("td")[5].get_text()

                if DX == '0':
                    DXstr = "DX0"
                else:
                    DXstr = "DX12"
                # print(branch + " " + Type + " " + Platform + " " + CPU + " " + GPU + " " + DXstr + " " + testsuite)
                conf = branch + " " + Type + " " + Platform + " " + CPU + " " + GPU + " " + DXstr + " " + testsuite
                if row.find_all('a'):
                    result_link = row.find_all('a')[0].get('href')
                    result_dict[conf] = result_link
    #print(result_dict)
    return result_dict

def get_specific_testCase_result(cmd,testlog):


    page_text=getPage(testlog)

    soup = BeautifulSoup(page_text, 'html.parser')
    #print(soup.get_text())
    result_list=soup.find_all("pre")[0].get_text()
    for i in result_list.split("\n"):
        if i.find(cmd)!=-1:
            #teseCaseResult=i.split(" ")[-1]
            teseCaseResult=i
            print("teseCaseResult",teseCaseResult)
            return teseCaseResult
    else:
        teseCaseResult="Not found the test case"
    print(teseCaseResult)
    return teseCaseResult


def get_testcase_result(uuid,configuration,testcase):
    print("uuid",uuid)
    # print("CCC",configuration)
    # print(testcase)
    uuid_link=uuid_link="http://scdvs.nvidia.com/Regression_Results?which_changelist="+uuid+"&which_page=current_regressions&which_category=Extended+Sanity"
    page_text = getPage(uuid_link)
    # test_links=get_all_tests(page_text)
    test_dict = get_specific_links(page_text)
    print(configuration)
    if configuration not in test_dict.keys():

        # print(test_dict.keys())
        result="Not found this configuration"
        return result
    # config = "cudnn_rc_hopper_cuda_11.8 Release RHEL8 64 amd_epyc7413_24c gh100_pg520_0201 DX12 CUDNN.LEVEL.TESTS.L4"
    # testcase = "cudnnTest -Rwgrad -n5 -Ps -algo1 -formatIn1 -filtFormat1 -formatOut1"
    # testcase="RNN -dataType1 -seqLength20 -numLayers2 -inputSize512 -hiddenSize512 -projSize512 -miniBatch64 -inputMode1 -dirMode0 -cellMode2 -biasMode3 -algorithm0"
    result = get_specific_testCase_result(testcase, test_dict[str(configuration)])
    print(result)
    return result



if __name__ == "__main__":
    page_text=getPage(uuid_link)
    test_links=get_all_tests(page_text)
    # test_dict=get_specific_links(page_text)
    # config="cudnn_rc_hopper_cuda_11.8 Release RHEL8 64 amd_epyc7413_24c gh100_pg520_0201 DX12 CUDNN.LEVEL.TESTS.L4"
    # testcase="cudnnTest -Rwgrad -n5 -Ps -algo1 -formatIn1 -filtFormat1 -formatOut1"
    # #testcase="RNN -dataType1 -seqLength20 -numLayers2 -inputSize512 -hiddenSize512 -projSize512 -miniBatch64 -inputMode1 -dirMode0 -cellMode2 -biasMode3 -algorithm0"
    # result=get_specific_testCase_result(testcase,test_dict[config])

    total_spend=0

    for page in test_links:
        #page_text=getPage("http://scvrlweb.nvidia.com/showjob.php?job=9468651")
        page_text=getPage(page)
        duration=content_analysis(page_text)
        total_spend += duration

    print(total_spend)
    print("Total spend %d hours"%(total_spend/60))
