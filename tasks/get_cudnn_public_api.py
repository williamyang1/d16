from bs4 import BeautifulSoup
import requests
cudnn_doc_url='https://docs.nvidia.com/deeplearning/cudnn/api/index.html'
section ={
    'ops_infer': '3.2',
    # 'ops_train': '4.1',
    # 'cnn_infer': '5.2',
    # 'cnn_train': '6.2',
    # 'adv_infer': '7.2',
    # 'adv_train': '8.2',
}

class CuDNNApi:
    api_name=""
    is_deprecated = False
deprecated = 'This function has been deprecated in cuDNN'

def get_soup():
    response = requests.get(cudnn_doc_url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def parse_cudnn_api(soup,section_number='3.2'):
    all_h3 = soup.find_all('h3', class_='title topictitle2')
    pub_api = []
    for h3 in all_h3[:40]:
        print("HHH3",h3)
        a = h3.a
        print("h3.a",a)
        if h3.a.text.startswith(section_number):
            kbd = h3.find('kbd', class_='ph userinput')
            print("text",h3.a.text)
            print("kbd",kbd)

            if kbd:  # should be API name
                cudnn_api = CuDNNApi()
                cudnn_api.api_name = kbd.text.replace('()', '')
                # pub_api.append(api_name)
                all_p = h3.parent.find_all('p')
                print("all p",all_p)
                for p in all_p:
                    if deprecated in p.text:
                        # todo, set api property here
                        cudnn_api.is_deprecated = True
                pub_api.append(cudnn_api)
    return pub_api

def get_cudnn_api():
    soup=get_soup()
    pub_api=[]
    for k,v in section.items():
        pub_api+=parse_cudnn_api(soup,v)

def main():
    get_cudnn_api()
if __name__ == '__main__':
    main()
