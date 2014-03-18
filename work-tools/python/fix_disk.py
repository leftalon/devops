#!/usr/bin/env python
#encoding:utf-8
import os

f=open("/proc/mounts")
mnt_list=['data0','data1','data2','data3','data4','data5','data6','data7','data8','data9','data10','data11']


def mount(dev,mnt):
        dev = dev
        mnt = mnt
        p = os.popen("fuser -m /%s" %mnt).read()
        for pid in p.split():
            os.system("kill -9 %s" %pid)
        os.system("umount /%s" %mnt)
        os.system("mkfs.ext3 %s" %dev)
        os.system("mount %s /%s" %(dev,mnt))
        os.system("chown -R daemon:daemon /%s" %mnt)
for i in f.read().split("\n"):
        line = i.strip().split()
        if len(line) != 0:
                dev = line[0]
                mnt = line[1].split("/")[-1]
                statu = line[3].split(",")[0]
                if statu != 'rw' and mnt in mnt_list:
                    print "%s filesystem is error" %dev
                    c = mount(dev,mnt)
		    if c:
			if mnt == "data0":
			    os.system("mkdir -p /data0/log/dip")
		            os.system("mkdir -p /data0/log/nginx")	
                    os.system("puppet agent -t")
