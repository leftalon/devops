#!/usr/bin/env python
# encoding:utf-8
# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from aomp.cmdb.models import Game_name_all,Server_all
from aomp.cmdb.models import Server_game_group
from salt_command import Query_salt_client,All_minion_basic_message,Mionin_key
import os
#define command
command_list = ['cmd.run','test.ping','disk.usage','grains.items','grains.item']

@login_required
def command(request):
    game_items_list = []
    game_group_list = [] 
    result = []
    arg_dict = {}
    saltgroup = "ALL"
    saltitems = "ALL"
    arg1 = "test.ping"
    arg2 = ''
    game_all = Game_name_all.objects.all()
    group_all = Server_game_group.objects.all()
    for game_message in game_all:
        if game_message.game_name not in game_items_list:
            game_items_list.append(game_message.game_name)
    for group_message in group_all:
        if group_message.group_name not in game_group_list:
            game_group_list.append(group_message.group_name)
    if request.method == "POST":
        saltitems = request.POST.get("saltitems")
        saltgroup = request.POST.get("saltgroup")
        arg1 = request.POST.get("arg1")
        arg2 = request.POST.get("arg2",'')
        arg_dict["saltitems"] = saltitems
        arg_dict["saltgroup"] = saltgroup
        arg_dict["arg1"] = arg1
        arg_dict["arg2"] = arg2
        result = Query_salt_client(arg_dict)
    return render_to_response("salt_auto/command_page.html",{'game_group_list':game_group_list,'command_list':command_list,'game_items_list':game_items_list,'result':result,'saltitems':saltitems,'saltgroup':saltgroup,'arg1':arg1,'arg2':arg2},context_instance=RequestContext(request))

@login_required
def minion(request):
    cmdb_saltaccept_unaccept_num = []
    install_salt = []
    uninstall_salt = []
    cmdb_all_server = []
    server_all = Server_all.objects.all()
    all_minion_message = All_minion_basic_message()
    server_all_num = server_all.count()
    mionin_key_dict = Mionin_key()
    #得到cmdb中所有机器
    for server_message in server_all:
        if server_message.server_id not in cmdb_all_server:
            cmdb_all_server.append(server_message.server_id)
    #所有安装salt的机器
    install_salt = mionin_key_dict["minions"] + mionin_key_dict["minions_pre"]
    #cmdb - 安装salt的机器 = 未安装salt的机器
    for host_name in cmdb_all_server:
        if host_name not in install_salt:
            uninstall_salt.append(host_name)
    if mionin_key_dict:
        mionin_accept = mionin_key_dict["minions"]
        if mionin_accept:
            mionin_accept_num = len(mionin_accept)
        else:
            mionin_accept_num = 0
        mionin_unaccept = mionin_key_dict["minions_pre"]
        if mionin_unaccept:
            mionin_unaccept_num = len(mionin_unaccept)
        else:
            mionin_unaccept_num = 0
    else:
        mionin_accept_num = 0
        mionin_unaccept_num = 0
    cmdb_saltaccept_unaccept_num.append(["cmdb_total(%d)"%server_all_num,server_all_num])
    cmdb_saltaccept_unaccept_num.append(["mionin_accept(%d)"%mionin_accept_num, mionin_accept_num])
    cmdb_saltaccept_unaccept_num.append(["mionin_unaccept(%d)"%mionin_unaccept_num,mionin_unaccept_num])
    if request.method == "POST":
        #添加认证处理
        add_host = request.POST.get("unaccept_host")
        if add_host == "all":
            unaccept_all = mionin_key_dict["minions_pre"]
            for unaccept_fqdn in unaccept_all:
                os.system("salt-key -a %s -y" %unaccept_fqdn)
        else:
            unaccept_fqdn = add_host
            os.system("salt-key -a %s -y" %unaccept_fqdn)
        
        #安装salt软件处理
        install_salt = request.POST.get("un_salt")
        if install_salt == "all":
            unin_salt = uninstall_salt
            for un_s in unin_salt:
                print un_s
        else:
            un_s = install_salt
            print un_s
        
        #删除认证处理
        del_host = request.POST.get("accept_host")
        if del_host == "all":
            accept_all = mionin_key_dict["minions"]
            for accept_fqdn in accept_all:
                os.system("salt-key -d %s -y" %accept_fqdn)
        else:
            accept_fqdn = del_host
            os.system("salt-key -d %s -y" % accept_fqdn)
        return HttpResponseRedirect("/salt_auto/minion")
    return render_to_response("salt_auto/minion_page.html",{'uninstall_salt':uninstall_salt,'mionin_key_dict':mionin_key_dict,'cmdb_saltaccept_unaccept_num':cmdb_saltaccept_unaccept_num,'all_minion_message':all_minion_message},context_instance=RequestContext(request))
