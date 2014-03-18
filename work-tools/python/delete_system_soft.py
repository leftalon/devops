#!/usr/bin/env python
#encoding:utf-8
import os
role ={'bk':["nginx","pdns"],'ts':[1,2],'ha':[3,4],'esngx':[5,6]}

def umount_disk(mnt):
        mnt = mnt
        p = os.popen("fuser -m %s" %mnt).read()
        for pid in p.split():
            os.system("kill -9 %s" %pid)
        os.system("umount %s" %mnt)


def rm_soft(soft):
    os.system("yum -y remove %s" %soft)


need_umount_disk = os.popen("df -h|grep data|awk '{print $NF}'").read()

for mnt in need_umount_disk.split():
#    umount_disk(mnt)
try:
    role_name = os.popen("hostname").read().split(".")[2]
except:
    print "hostname is error"

if role_name in role:
    remove_soft = rolae[role_name]
    for soft in remove_soft:
 #       rm_soft(soft)

