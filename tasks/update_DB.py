import json
from django.db import models
from app01 import models

def UUID_DB_update():
    from app01.tasks.get_uuid import get_version_list
    version_prefix="8.6.0."
    branch="cudnn_rc_hopper_cuda_11.8"
    version_list=get_version_list(branch)
    for (uuid,cl,version) in version_list:
        print(uuid,cl,version)
        version = version_prefix + str(version)
        if models.UUID.objects.filter(UUID=uuid).exists():
            print("UUID exist")
            continue
        models.UUID.objects.create(UUID=uuid, CL=cl, version=version)


def update():
    UUID_DB_update()


if __name__ == '__main__':
    update()