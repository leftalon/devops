#!/usr/bin/env python
#encoding:utf-8
# Create your views here.
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from aomp.cmdb.models import Server_all
from role_config_message import test1_node_config
from aomp.puppet_config.models import Node_config_message
from aomp.cmdb.pagination import pagination_django
from django.db.models import Q
from django.http import HttpResponseRedirect
#defined variable
puppet_node_dir = "/etc/puppet/node/"
page_value = 15.0

@login_required
def puppet(request):
    search_text=''
    puppet_server_all = Node_config_message.objects.all()
    puppet_server_num = puppet_server_all.count()
    if request.method == "GET":
        page_num = request.GET.get("page",1)
        if page_num != "all":
            page_num = int(page_num)
        search_text = request.GET.get("search_text",'')
        if search_text == '' or search_text == None:
            puppet_server = puppet_server_all
        else:
            puppet_server = Node_config_message.objects.filter(Q(node_name__icontains=search_text) | Q(private_ip__icontains=search_text) | Q(public_ip__icontains=search_text) | Q(node_file__icontains=search_text) | Q(items_name__icontains=search_text) | Q(group_name__icontains=search_text))
        page_start_end,page_up,page_next,first_page,last_page,puppet_all_data,last_page_value = pagination_django(puppet_server,page_value,page_num)
    return render_to_response('puppet_config/puppet_frist_page.html',{'page_num':page_num,'last_page_value':last_page_value,'puppet_all_data':puppet_all_data,'page_list':page_start_end,'page_up':page_up,'page_next':page_next,'first_page':first_page,'last_page':last_page,'search_text':search_text},context_instance=RequestContext(request))

@login_required
def node_pp_config(request,node_id):
    node_server_message = Node_config_message.objects.filter(id=node_id)
    return render_to_response('puppet_config/node_pp_config.html',{'node_server_message':node_server_message},context_instance=RequestContext(request))

@login_required
def host_config_add(request):
    message = ''
    node_config = ''
    node_name = ''
    server_message = ''
    server_all = Server_all.objects.all()
    if request.method == "POST":
        node_name = request.POST.get("node_name",None)
        server_message = request.POST.get("server_message",None)
        if node_name == None or node_name == '':
            message = u'Node name不能为空'
        elif Node_config_message.objects.filter(node_name=node_name):
            message = u"Node name已经存在"
        else:
            node_server_message  = Server_all.objects.filter(server_id = server_message)
            if node_server_message:
                for node_message in node_server_message:
                    cmdb_id = node_message.id
                    private_ip = node_message.server_in_ip
                    public_ip = node_message.server_out_ip
                    items_name = node_message.server_product
                    group_name = node_message.server_group
                    node_config = test1_node_config(node_name,private_ip,public_ip,items_name,group_name)
                    if Node_config_message.objects.filter(cmdb_id=cmdb_id):
                        message = u"该机器的Node File已经存在"
                    else:
                        node_sql = Node_config_message(node_name=node_name,cmdb_id=cmdb_id,items_name=items_name,group_name=group_name,private_ip=private_ip,public_ip=public_ip,node_file=node_config)
                        if node_sql:
                            try:
                                node_sql.save()
                                message = u"access"
                            except Exception,e:
                                message = e
                        else:
                            message = u"请检查你的sql!"
            else:
                message = u'请检查CMDB中该机器信息是否正确'
    return render_to_response('puppet_config/host_config_add.html',{'server_message':server_message,'node_name':node_name,'node_config':node_config,'server_all':server_all,'message':message},context_instance=RequestContext(request))

@login_required
def delete_node_id(request,node_id):
    message = ''
    node_id = int(node_id)
    if request.method == "GET":
        del_server = Node_config_message.objects.filter(id=node_id)
        if del_server:
            try:
                del_server.delete()
                return HttpResponseRedirect("/puppet")
            except Exception,e:
                message = e
    return HttpResponseRedirect("/puppet")

@login_required
def update_node_id(request,cmdb_id):
    if request.method == "GET":
        update_server = Server_all.objects.filter(id=cmdb_id)
        node_server = Node_config_message.objects.filter(cmdb_id=cmdb_id)
        if node_server:
            for node in node_server:
                node_name = node.node_name
        if update_server:
            for node_message in update_server:
                private_ip = node_message.server_in_ip
                public_ip = node_message.server_out_ip
                items_name = node_message.server_product
                group_name = node_message.server_group
                node_config = test1_node_config(node_name,private_ip,public_ip,items_name,group_name)
                if Node_config_message.objects.filter(cmdb_id=cmdb_id).update(node_name=node_name,items_name=items_name,group_name=group_name,private_ip=private_ip,public_ip=public_ip,node_file=node_config):
                    return HttpResponseRedirect("/puppet")
    return HttpResponseRedirect("/puppet")
