#!/usr/bin/env python
# encoding:utf-8
'''
ip库格式
cat ipseg.txt
192.168.1.1 192.169.1.2 中国-电信-上海
192.169.1.3 192.190.1.9 中国-网通-上海
'''
#import module
import bisect
import socket
import struct

#ip change int after dict
ip2int_dict = {
	#3232235777:(3232235777,3232301314,"中国-电信-上海")
	#3232301315:(3232301315,3233677577,"中国-网通-上海")
}

ip2int_start_list = []

ip2int_len = len(ip2int_start_list)

#ip change int
def ip2int(ip_address):
	global ipstr
	ipstr = struct.unpack("!I",socket.inet_aton(ip_address))[0]
	return ipstr

def init(ip_file):
	file_line = open(ip_file)
	for line in file_line.read().split("\n"):
		if len(line.strip()) == 0:
			continue
		else:
			line = line.split()
			start_ip = ip2int(line[0])
			end_ip = ip2int(line[1])
			location = line[2]	
			if start_ip in ip2int_dict:
				continue
			else:
				ip2int_dict[start_ip] = (start_ip,end_ip,location)
	for startip in ip2int_dict:
		ip2int_start_list.append(startip)
	ip2int_start_list.sort()
	return ip2int_dict
	return ip2int_start_list
		
			
def searchip(ip):
	global location
	ip = ip.strip()
	ip_to_int = ip2int(ip)
	if ip2int_dict.get(ip_to_int):
		location = ip2int_dict[ip_to_int][2]
	else:
		i = bisect.bisect_left(ip2int_start_list,ip_to_int)
		if i > ip2int_len and i == 0:
			location = "unknow"
		else:
			start_ip = ip2int_start_list[i-1]
			location = ip2int_dict[start_ip][2]
	return location
	
if __name__ == "__main__":
	ip_file = "ipseg.txt"
	init(ip_file)
	print "192.168.1.1 "+searchip("192.168.1.1")
	print "192.169.1.23 "+searchip("192.169.1.23")

'''
打印结果：
192.168.1.1 中国-电信-上海
192.169.1.23 中国-网通-上海
'''
