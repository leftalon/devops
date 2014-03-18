#!/bin/sh

cat > dev_mount << EOF
/dev/sda 0
/dev/sdb 1
/dev/sdc 2
/dev/sdd 3
/dev/sde 4
/dev/sdf 5
/dev/sdg 6
/dev/sdh 7
/dev/sdi 8
/dev/sdj 9
/dev/sdk 10
/dev/sdl 11
EOF

MegaCli="/opt/MegaRAID/MegaCli/MegaCli64"

disk_count=`$MegaCli -PDlist  -aALL|grep "Device Id"|wc -l`
disk_0_9=`expr $disk_count - 1`
fdisk_count=`fdisk -l|grep Disk|grep -v identifier|wc -l`
fdisk -l|grep Disk|grep -v identifier|awk -F[": "] '{print $2}' > fdisk_dev.txt

if [ $disk_count == $fdisk_count ];then
	echo "The DISK total $disk_count all ok"
else
	for i in `seq 0 $disk_0_9`
	do
		disk=`cat dev_mount|awk -v count=$i '{if(count==$2) print $1}'`
		grep "$disk" fdisk_dev.txt >/dev/null 2>&1
		if [ `echo $?` != 0 ];then
			echo $disk
		fi
	done
	
fi
