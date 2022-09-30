from P4 import P4
import os
cudnn_dir = r'//sw/gpgpu/MachineLearning/cudnn'
def get_p4_info():
    p4 =P4()
    p4.port="p4proxy-zj:2006"
    p4.user = "williamy"
    p4.client="williamy_202105"
    try:
        p4.connect()
        info = p4.run('info')
        #info = p4.run('p4 changes -m3 //sw/gpgpu/MachineLearning/cudnn_v8.6/...')
        print(info)
    except Exception:
        print('Fail to connect to p4 server')
        exit(-1)
    return info


if __name__ == '__main__':
    info = get_p4_info()
    p4root = info[0].get('clientRoot')
    cudnn_local_dir = p4root + cudnn_dir.replace('//', '/')
    cudnn_local_test_dir = os.path.join(cudnn_local_dir, 'test')
    print(p4root)
    print(cudnn_local_test_dir)

