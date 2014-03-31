#!/usr/bin/python
# encoding: utf-8
__authors__ = ['left']
__version__ = 1.0
__date__    = '2014-03-18 10:28:40'
__licence__ = 'GPL licence'

#import modules
import salt
from aomp.cmdb.models import Server_all
import salt.wheel
#defined variable
salt_master_config_dir = "/etc/salt/master"

#command message
def Query_salt_client(args):
    #定义一个结果列表
    global result
    result = []
    salt_frist_arg = salt.client.LocalClient()
    #取全部服务器的信息
    if args["saltitems"] == "ALL" and args["saltgroup"] == "ALL":
        host_all = Server_all.objects.all()
        arg1 = args["arg1"]
        arg2 = args["arg2"]
        if host_all:
            for server_message in host_all:
                hostmsg = server_message.server_id
                #判断arg2是否为空
                if arg2.strip():
                    arg2 = list(arg2.split(","))
                    result_temp = salt_frist_arg.cmd(hostmsg,arg1,arg2)
                    result.append(result_temp)
                else:
                    result_temp = salt_frist_arg.cmd(hostmsg,arg1)
                    result.append(result_temp)
    
    #取单个组的所有信息
    elif args["saltitems"] == "ALL" and args["saltgroup"] != "ALL":
        server_group = args["saltgroup"]
        arg1 = args["arg1"]
        arg2 = args["arg2"]
        #查询数据中该组的所有机器
        group_host_all = Server_all.objects.filter(server_group=server_group)
        #判断数据库中是否有数据
        if group_host_all:
            #循环得到查询的数据
            for server_message in group_host_all:
                hostmsg = server_message.server_id
                if arg2.strip():
                    arg_command = list(arg2.split(","))
                    result_temp = salt_frist_arg.cmd(hostmsg,arg1,arg_command)
                else:
                    result_temp = salt_frist_arg.cmd(hostmsg,arg1)
            result.append(result_temp)
    
    #取单个项目的所有机器信息
    elif args["saltitems"] != "ALL" and args["saltgroup"] == "ALL":
        server_items = args["saltitems"]
        arg1 = args["arg1"]
        arg2 = args["arg2"]
        items_host_all = Server_all.objects.filter(server_product=server_items)
        if items_host_all:
             #循环得到查询的数据
            for server_message in items_host_all:
                hostmsg = server_message.server_id
                if arg2.strip():
                    arg_command = list(arg2.split(","))
                    result_temp = salt_frist_arg.cmd(hostmsg,arg1,arg_command)
                    print result_temp
                else:
                    result_temp = salt_frist_arg.cmd(hostmsg,arg1)        
            result.append(result_temp)
    
    #取单个项目单个组的机器信息    
    else:
        server_group = args["saltgroup"]
        server_items = args["saltitems"]
        arg1 = args["arg1"]
        arg2 = args["arg2"]
        items_group_host_all = Server_all.objects.filter(server_product=server_items,server_group=server_group)
        if items_group_host_all:
            for server_message in items_group_host_all:
                hostmsg = server_message.server_id
                if arg2.strip():
                    arg_command = list(arg2.split(","))
                    result_temp = salt_frist_arg.cmd(hostmsg,arg1,arg_command)
                else:
                    result_temp = salt_frist_arg.cmd(hostmsg,arg1)        
            result.append(result_temp)
    return result

#query all minion basic message
def All_minion_basic_message():
    global all_basic_message
    all_basic_message = {}
    salt_client = salt.client.LocalClient()
    all_basic_message = salt_client.cmd('*','grains.items')
    return all_basic_message

def Mionin_key():
    global mionin_key_list
    mionin_key_dict = {}
    salt_master_config = salt.config.master_config(salt_master_config_dir)
    mionin_key = salt.wheel.Wheel(salt_master_config)
    mionin_key_dict = mionin_key.call_func('key.list_all')
    return mionin_key_dict

