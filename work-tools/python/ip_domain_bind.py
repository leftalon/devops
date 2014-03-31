#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2014-03-29 10:53:40'
__licence__	= 'GPL licence'


'''
该接口的用法:
注意:同目录下有一个domain.txt的配置文件
1、绑定域名、ip、端口，需要编辑domian.txt文件，格式如下：
    a、domain:ip:port           （绑定一个端口）
    b、domain:ip:port1|port2    （绑定多个端口）

2、解绑域名，需要编辑domain.txt文件，格式如下：
    a、domain::                 （解绑该域名的所有ip、端口）
    b、domain:ip:               （解绑该域名该ip的所有端口）
    c、domain::port             （解绑该域名的所有ip的某个端口）
    d、domain:ip:port           （解绑该域名该ip的该端口）
    e、domian:ip:port1|port2    （解绑该域名该ip的某些端口）

3、配置文件都ok后执行下面的command:
    a、python ip_domain_bind.py on      绑定
    b、python ip_domain_bind.py off     解绑
    c、python ip_domain_bind.py index   查询

'''

import time
import urllib2
import random
import base64
import json
import hmac
import hashlib
import urllib
import sys
"""
orignal 
body=&method=GET&uri=/cvms&x-txc-cloud-secretid=EEJqoOlMV5BLXCN9xm7tCe4wJDKKqyTI&x-txc-cloud-nonce=15846216&x-txc-cloud-timestamp=1356019200
"""
#初始化header信息，得到api取数据的字段信息
class API_Init:
    def __init__(self):
        self.secretID = "n"
        self.secretKEY = "n"    #腾讯平台上设置对应的key和id
        self.api_domain = "https://api.yun.qq.com"
        self.nonce = random.randint(1,31)
        self.timestr = int(time.time())
        self.uri = ''
        self.body = ''
        self.method = ''

    def set_body(self,value):
        self.body = value
        return self.body

    def set_method(self,value):
        self.method = value
        return self.method

    def set_uri(self,value):
        self.uri = value
        return self.uri

    def do_request(self):
        if self.body:
            data = json.dumps(self.body)
        else:
            data = self.body
        self.orignal = "body=%s&method=%s&uri=%s&x-txc-cloud-secretid=%s&x-txc-cloud-nonce=%s&x-txc-cloud-timestamp=%s" %(data,self.method,self.uri,self.secretID,self.nonce,self.timestr)
        self.sign = base64.b64encode(hmac.new(self.secretKEY,self.orignal,digestmod=hashlib.sha1).digest())
        header_data = {
                "x-txc-cloud-secretid":self.secretID,
                "x-txc-cloud-nonce":self.nonce,
                "x-txc-cloud-timestamp":self.timestr,
                "x-txc-cloud-signature":self.sign,
        }
        url = self.api_domain + self.uri
        if self.body:
            self.req = urllib2.Request(url,data)
        else:
            self.req = urllib2.Request(url)
        for key in header_data:
            self.req.add_header(key,header_data[key])
        try:
            result = urllib2.urlopen(self.req)
            return result
        except Exception,e:
            print e

#查询域名信息
def index_domain(domain):
    global access_domain,error_domain
    access_domain = []
    exist_domain = []
    api = API_Init()
    if domain:
        api.set_uri("/v1/domains/query_instance_id?domains=%s" %domain)
        api.set_method("GET")
        result = api.do_request()
        if result:
            for line in result.readlines():
                lines = json.loads(line)
                if len(lines["instanceIds"]) == 0 and lines["httpCode"] == 200:
                    access_domain.append(domain)
                elif len(lines["instanceIds"]) != 0 and lines["httpCode"] == 200:
                    d_id = lines["instanceIds"]
                    exist_domain.append(d_id)
                else:
                    pass
    return access_domain,exist_domain

#查询资源ID
def get_instaceid(domain):
    instanceId = 0
    api = API_Init()
    if domain:
        api.set_uri("/v1/domains/query_instance_id?domains=%s" %domain)
        api.set_method("GET")
        result = api.do_request()
        if result:
            for line in result.readlines():
                lines = json.loads(line)
                if len(lines["instanceIds"]) > 0 and lines["httpCode"] == 200:
                    instanceId = lines["instanceIds"][domain]
    return instanceId

#创建域名信息
def create_domain(access_domain):
    global create_domain_access,create_domain_error 
    create_domain_access = []
    create_domain_error = []
    temp_domain_dict = {}
    for domain in access_domain:
        api = API_Init()
        api.set_uri("/v1/domains")
        api.set_method("POST")
        body = {"domain":domain}
        api.set_body(body)
        result = api.do_request()
        if result:
            for line in result.readlines():
                temp_content = json.loads(line)
                if temp_content["httpCode"] == 200 and len(temp_content["instances"]) != 0:
                    temp_domain_dict[domain] = temp_content["instances"][0]["instanceId"]
                    create_domain_access.append(temp_domain_dict)
                else:
                    create_domain_error.append(domain)
    return create_domain_access

#绑定域名信息
def bind_ip_port_domain(ip,port,instanceId):
    api = API_Init()
    api.set_uri("/v1/domains/%d/cvm_bind" %instanceId)
    body_dict = {"lanIps":[ip],"port":port}
    api.set_body(body_dict)
    api.set_method("POST")
    result = api.do_request()
    if result:
        for line in result.readlines():
            print line

#解绑域名信息
def unbind_ip_port_domain(ip,port,instanceId):
    api = API_Init()
    api.set_uri("/v1/domains/%d/cvm_unbind" %instanceId)
    body_dict = {"devicesList":[{"lanIp":ip,"port":port}]}
    api.set_body(body_dict)
    api.set_method("POST")
    result = api.do_request()
    if result:
        for line in result.readlines():
            print line

#查询域名绑定情况
def query_domain_detail(instanceId):
    api = API_Init()
    api.set_uri("/v1/domains/%d" %instanceId)
    api.set_method("GET")
    result = api.do_request()
    ip_port = []
    if result:
        for line in result.readlines():
            temp_content = json.loads(line)
            if temp_content['httpCode'] == 200 and len(temp_content['instanceInfo']) > 0:
                ip_port = temp_content['instanceInfo']['devicesList']
    return ip_port
    

def main():
    status = sys.argv[1]
    open_file = open("domain.txt")
    for domain_m in open_file:
        bind_port = []
        domain_list = domain_m.strip().split(":")
        domain = domain_list[0]
        bind_ip = domain_list[1]
        if domain_list[2]:
            bind_port = domain_list[2].split("|")
        if status == "on":
            access_domain,exist_domain = index_domain(domain)
            if access_domain:
                create_domain_access = create_domain(access_domain)
                if create_domain_access:
                    for port_m in bind_port:
                        port = int(port_m)
                        ip = bind_ip
                        domain = domain
                        instanceId = int(create_domain_access[0][domain])
                        bind_result = bind_ip_port_domain(ip,port,instanceId)
                        time.sleep(60)
            elif exist_domain:
                for port_m in bind_port:
                    port = int(port_m)
                    ip = bind_ip
                    domain = domain
                    print port
                    instanceId = int(exist_domain[0][domain])
                    bind_result = bind_ip_port_domain(ip,port,instanceId)
                    time.sleep(60)
        if status == "off":
            access_domain,exist_domain = index_domain(domain)
            if exist_domain:
                instanceId = int(exist_domain[0][domain])
                if not (bind_ip and bind_port):
                    ip_port = query_domain_detail(instanceId)
                    temp_ip_port = []
                    if not bind_ip and bind_port:
                        for i in ip_port:
                            if str(i['port']) in bind_port:
                                temp_ip_port.append(i)
                    elif not bind_port and bind_ip:
                        for i in ip_port:
                            if i['lanIp'] == bind_ip:
                                temp_ip_port.append(i)
                    if temp_ip_port:
                        ip_port = temp_ip_port
                    print ip_port
                    for each in ip_port:
                        ip = each['lanIp']
                        port = int(each['port'])
                        unbind_result = unbind_ip_port_domain(ip,port,instanceId)
                        time.sleep(60)
                else:
                    for port_m in bind_port:
                        port = int(port_m)
                        ip = bind_ip
                        unbind_result = unbind_ip_port_domain(ip,port,instanceId)
                        time.sleep(60)
        if status == "index":
            instanceId = get_instaceid(domain)
            if instanceId > 0:
                ip_port = query_domain_detail(instanceId)
                if not ip_port:
                    print '%-50s%-20s%-10s' %(domain,'NoIP','NoPort')
                else:
                    for each in ip_port:
                        print '%-50s%-20s%-10s' %(domain,each['lanIp'],each['port'])
            else:
                print '%-50s%-20s%-10s' %(domain,'NoIP','NoPort')
            print "-"*100
            time.sleep(1)

if __name__ == "__main__":
    main()

