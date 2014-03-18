#!/bin/bash
#set valiable
disk=`fdisk -l|grep -E "sda7|sd.1"|grep -v sda1|awk '{print $1}'`
mnt_disk=`df -h|grep data|awk '{print $1}'`

#set dev vs mnt
#dev vs mnt
cat > dev_mnt.txt << EOF
/dev/sda7 /data0
/dev/sdb1 /data1
/dev/sdc1 /data2
/dev/sdd1 /data3
/dev/sde1 /data4
/dev/sdf1 /data5
/dev/sdg1 /data6
/dev/sdh1 /data7
/dev/sdi1 /data8
/dev/sdj1 /data9
/dev/sdk1 /data10
/dev/sdl1 /data11 
EOF


function nginx_disk_mount {
for i in $disk
do
	if [ $mnt_disk ! = "" ];then
		for j in $mnt_disk
		do
			if [ $i = $j ];then
				echo "$i is mount"
			else
				mnt_dir=`cat dev_mnt.txt|grep $i|awk '{print $2}'`
				mount $i /$mnt_dir && chown -R daemon:daemon /$mnt_dir
			fi
		done
	else
		mnt_dir=`cat dev_mnt.txt|grep $i|awk '{print $2}'`
		mount $i /$mnt_dir && chown -R daemon:daemon /$mnt_dir
	fi
done
}

