#!/usr/bin/python
# encoding: utf-8
__authors__ = ['left']
__version__ = 1.0
__date__    = '2013-10-19 11:38:23'
__licence__ = 'GPL licence'

#import modules
from django.shortcuts import render_to_response
from aomp.cmdb.models import Server_all
from aomp.cmdb.models import Game_name_all
from aomp.cmdb.models import Server_platform
from aomp.cmdb.models import IDC_name_all,Server_type_all,Server_game_group
from aomp.cmdb.models import Event_record
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from aomp.cmdb.server_status import server_status_list
from django.core.paginator import Paginator
from aomp.cmdb.variable_db import variable_db_dict
from aomp.cmdb.server_search import server_search
from aomp.cmdb.server_search import fan_search
from django.contrib.auth.models import User,Group,Permission
from aomp.cmdb.permission_auth import permission_auth
from django.db.models import Q
from aomp.cmdb.server_search import server_search_dict
from math import ceil
from aomp.cmdb.query_server_message import query_server_message
from aomp.cmdb.pagination import pagination
from aomp.cmdb.pagination import pagination_django
from aomp.cmdb.operation_models import operation_models
from aomp.cmdb.models import Server_template
from aomp.cmdb.models import Game_type_name
from aomp.cmdb.server_template_dict import server_template_dict
import time,datetime
import re
#defined global variable
#page_value分页数
page_value = 15.0

server_groups = Server_game_group.objects.all()
#所有访问没权限的页面都会返回到这个页面
@login_required
def home(request):
    return render_to_response("cmdb/home.html",{},context_instance=RequestContext(request))


@login_required
def frist_page(request):
    data = []
    game_num = Game_name_all.objects.all()
    for game_message in game_num:
        game_name = game_message.game_name
        data.append([game_name,1])
        data = data[:6]
    return render_to_response("cmdb/frist_page.html",{'data':data},context_instance=RequestContext(request))

#查询所有服务器
@login_required
#匹配权限
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def query_server(request):
    a_server = {}
    ip_server_dict = {}
    template_all_dict = server_template_dict()
    if request.method == "GET":
        object_admin = Game_name_all.objects.all()
        page_num = request.GET.get('page',1)
        if page_num != "all":
            page_num = int(page_num)
        search_text = request.GET.get('search_text','')
        game_type = request.GET.get('game_type','')
        if search_text == None or search_text == '':
            #通过内外网ip进行去重
            distinct_server = Server_all.objects.values("server_in_ip","server_out_ip","server_product").distinct()
            #all_server,ip_server_dict = query_server_message(distinct_server,game_type)
            all_server = query_server_message(distinct_server,game_type)
            #全部服务器的条数
            distinct_server_page = len(all_server)
            #可以分多少页
            page_v = int(ceil(distinct_server_page/page_value))
            page_list = [x+1 for x in range(page_v)]
            #分页key list
            key_list = []
            for k in all_server:
                key_list.append(k)
            #分页页码展示
            page_start_end,page_up,page_next,first_page,last_page,last_page_value = pagination(page_list,page_num)
            #分页数据提取
            if page_num == "all":
                a_server = all_server
            elif page_num == int(last_page_value):
                value_start = (page_num - 1) * int(page_value)
                value_end = distinct_server_page
                for key_ip in key_list[value_start:value_end]:
                    if key_ip in a_server:
                        continue
                    else:
                        a_server[key_ip] = all_server[key_ip]
            else:
                value_start = (page_num - 1) * int(page_value)
                value_end = page_num * int(page_value)
                for key_ip in key_list[value_start:value_end]:
                    if key_ip in a_server:
                        continue
                    else:
                        a_server[key_ip] = all_server[key_ip]
        else:
            #如果搜索先范搜索全部
            search_server = fan_search(search_text)
            #查询去重
            distinct_server = search_server.values("server_in_ip","server_out_ip","server_product").distinct()
            #all_server,ip_server_dict = query_server_message(distinct_server,game_type)
            all_server = query_server_message(distinct_server,game_type)

            distinct_server_page = len(all_server)
            #可以分多少页
            page_v = int(ceil(distinct_server_page/page_value))
            page_list = [x+1 for x in range(page_v)]
            #分页key list
            key_list = []
            for k in all_server:
                key_list.append(k)
            #分页页码展示
            page_start_end,page_up,page_next,first_page,last_page,last_page_value = pagination(page_list,page_num)
            #分页数据提取
            if page_num == "all":
                a_server = all_server
            elif page_num == int(last_page_value):
                value_start = (page_num - 1) * int(page_value)
                value_end = distinct_server_page
                for key_ip in key_list[value_start:value_end]:
                    if key_ip in a_server:
                        continue
                    else:
                        a_server[key_ip] = all_server[key_ip]
            else:
                value_start = (page_num - 1) * int(page_value)
                value_end = page_num * int(page_value)
                for key_ip in key_list[value_start:value_end]:
                    if key_ip in a_server:
                        continue
                    else:
                        a_server[key_ip] = all_server[key_ip]
        for k,v in a_server.items():
            server_list = []
            for s in v:
                for i in range(len(s)):
                    server_list.append("%s %s" %(s[i].server_id,s[i].server_status))
                ip_server_dict[k] = server_list
    return render_to_response("cmdb/index_server.html",{'template_all_dict':template_all_dict,'page_up':page_up,'page_next':page_next,'first_page':first_page,'last_page':last_page,'last_page_value':last_page_value,'page_num':page_num,'search_text':search_text,'server_count':distinct_server_page,'page_list':page_start_end,'ip_server_dict':ip_server_dict,'object_admin':object_admin,'a_server':a_server,'game_type':game_type},context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
#in_ip内网ip，out_ip外网ip
def query_server_search(request,in_ip,out_ip):
    template_all_dict = server_template_dict()
    if in_ip == '0.0.0.0':
        in_ip = ''
    if out_ip == '0.0.0.0':
        out_ip = ''
    object_admin = Game_name_all.objects.all()
    all_server = Server_all.objects.filter(server_in_ip=in_ip,server_out_ip=out_ip)
    server_count = all_server.count()
    return render_to_response("cmdb/server_hefu_message.html",{'template_all_dict':template_all_dict,'server_count':server_count,'object_admin':object_admin,'a_server':all_server},context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
#field 字段，value名字
def field_show(request,field,value):
    Q_result = None
    a_server = {}
    kargs = {}
    ip_server_dict = {}
    template_all_dict = server_template_dict()
    if request.method == "GET":
        object_admin = Game_name_all.objects.all()
        page_num = request.GET.get('page',1)
        if page_num != "all":
            page_num = int(page_num)
        search_text = request.GET.get('search_text','')
        if search_text == None or search_text == '':
            all_server = server_search(field,value)
            yewu_name = value
            #查询去重
            distinct_server = all_server.values("server_in_ip","server_out_ip").distinct()
            distinct_server_page = all_server.values("server_in_ip","server_out_ip").distinct().count()
            #可以分多少页
            page_v = int(ceil(distinct_server_page/page_value))
            page_list = [x+1 for x in range(page_v)]
            #all_server,ip_server_dict = query_server_message(distinct_server,'')
            all_server = query_server_message(distinct_server,'')
            #分页页码展示
            page_start_end,page_up,page_next,first_page,last_page,last_page_value = pagination(page_list,page_num)
            #分页key list
            key_list = []
            for k in all_server:
                key_list.append(k)
                #分页信息提取
                if page_num == "all":
                    a_server = all_server
                elif page_num == int(len(page_list)):
                    value_start = (page_num - 1) * int(page_value)
                    value_end = distinct_server_page
                    for key_ip in key_list[value_start:value_end]:
                        if key_ip in a_server:
                            continue
                        else:
                            a_server[key_ip] = all_server[key_ip]
                else:
                    value_start = (page_num - 1) * int(page_value)
                    value_end = page_num * int(page_value)
                    for key_ip in key_list[value_start:value_end]:
                        if key_ip in a_server:
                            continue
                        else:
                            a_server[key_ip] = all_server[key_ip]
        else:
            yewu_name = u"搜索%s" %search_text
            all_server1 = server_search(field,value)
            message = search_text
            all_server = all_server1.filter(Q(server_id__icontains=message) | Q(server_in_ip__icontains=message) | Q(server_out_ip__icontains=message) | Q(server_template_id__contains=message) | Q(server_company__icontains=message) | Q(server_product__icontains=message) | Q(server_status__icontains=message) | Q(server_idc__icontains=message))
            #查询去重
            distinct_server = all_server.values("server_in_ip","server_out_ip").distinct()
            distinct_server_page = all_server.values("server_in_ip","server_out_ip").distinct().count()
            #可以分多少页
            page_v = int(ceil(distinct_server_page/page_value))
            page_list = [x+1 for x in range(page_v)]
            #all_server,ip_server_dict = query_server_message(distinct_server,'')
            all_server = query_server_message(distinct_server,'')
            #分页key list
            key_list = []
            for k in all_server:
                key_list.append(k)
            #分页页码展示
            page_start_end,page_up,page_next,first_page,last_page,last_page_value = pagination(page_list,page_num)
            #分页信息提取
            if page_num == "all":
                a_server = all_server
            elif page_num == int(len(page_list)):
                value_start = (page_num - 1) * int(page_value)
                value_end = distinct_server_page
                for key_ip in key_list[value_start:value_end]:
                    if key_ip in a_server:
                        continue
                    else:
                            a_server[key_ip] = all_server[key_ip]
            else:
                value_start = (page_num - 1) * int(page_value)
                value_end = page_num * int(page_value)
                for key_ip in key_list[value_start:value_end]:
                    if key_ip in a_server:
                        continue
                    else:
                        a_server[key_ip] = all_server[key_ip]
                    a_server[key_ip] = all_server[key_ip]
        for k,v in a_server.items():
            server_list = []
            for s in v:
                for i in range(len(s)):
                    server_list.append("%s %s" %(s[i].server_id,s[i].server_status))
                ip_server_dict[k] = server_list
    return render_to_response("cmdb/field_show.html",{'template_all_dict':template_all_dict,'page_up':page_up,'page_next':page_next,'first_page':first_page,'last_page':last_page,'last_page_value':last_page_value,'page_num':page_num,'search_text':search_text,'server_count':distinct_server_page,'page_list':page_start_end,'ip_server_dict':ip_server_dict,'object_admin':object_admin,'a_server':a_server},context_instance=RequestContext(request))

#单台服务器添加函数
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.add_server') == True,login_url='/home/')
def server_add(request):
    user_game_dict = {}
    message = ''
    in_ip_valid = True
    out_ip_valid = True
    idcall = IDC_name_all.objects.all()
    gameall = Game_name_all.objects.all()
    typeall = Server_type_all.objects.all()
    templateall = Server_template.objects.all()
    companyall = Server_platform.objects.all()
    regex=ur"^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)(:\d{1,})?$"
    server_id = ''
    server_in_ip = ''
    server_out_ip = ''
    server_type = ''
    server_template = ''
    server_idc_company = ''
    server_idc = ''
    server_company = ''
    server_product = ''
    server_group = ''
    server_status = ''
    server_start_date = ''
    template_name = ''
    company_idc_dict = {}
    company_list = []
    default_company = ''
    default_idc = []
    start_date_valid = True
    per_all = Permission.objects.all()
    user = str(request.user)
    for per in per_all:
        user_game_dict[per.codename] = per.name
    if user in user_game_dict:
        gameall = user_game_dict[user].split(" ")

    #获取IDC的信息
    idc_all_name = IDC_name_all.objects.all()
    for name in idc_all_name:
        if name.idc_company == None or name.idc_company == '':
            company_name = u"其他"
        else:
            company_name = name.idc_company

        if request.method == "POST":
            default_company = request.POST.get('idc_company',None)
        if not default_company or default_company == company_name:
            if not default_company:
                default_company = company_name
            default_idc.append(name.idc_name)

        if company_name not in company_list:
            company_list.append(company_name)
        if company_name not in company_idc_dict:
            company_idc_dict[company_name] = [name.idc_name]
        else:
            company_idc_dict[company_name] += [name.idc_name]

    if request.method == "POST":
        server_id = request.POST.get('server_id',None)
        server_in_ip = request.POST.get('server_in_ip',None)
        server_out_ip = request.POST.get('server_out_ip',None)
        if server_in_ip:
            if not re.match(regex,server_in_ip):
                in_ip_valid = False
                message=u"提供的内网ip地址非法"
        if server_out_ip:
            if not re.match(regex,server_out_ip):
                out_ip_valid = False
                message=u"提供的外网ip地址非法"
        server_type = request.POST.get('server_type',None)
        server_template = request.POST.get('server_template',None)
        server_idc_company = request.POST.get('idc_company',None)
        server_idc = request.POST.get('server_idc',None)
        server_company = request.POST.get('server_company',None)
        server_status = request.POST.get('server_status',None)
        server_product = request.POST.get('server_product',None)
        server_group = request.POST.get('server_group', None)
        server_start_date = request.POST.get('server_start_date',None)
        template_name = server_template.split("(")[0]
        if server_start_date:
            if len(server_start_date) != 10:
                start_date_valid = False
            start_date = server_start_date.split('-')
            if len(start_date) != 3 or len(start_date[0]) != 4 or len(start_date[1]) != 2 or len(start_date[2]) != 2:
                start_date_valid = False
        if server_id == None or server_id == '':
            message = u"服务器唯一id信息不能为空"
        elif not in_ip_valid:
            message=u"提供的内网ip地址不正确"
        elif not out_ip_valid:
            message=u"提供的外网ip地址不正确"
	elif len(server_id.split(".")) != 2:
	    message=u"请检查服务器唯一id"
        elif not start_date_valid:
            message = u"服务器开始时间无效"
        else:
            re_server_id = ''
            if IDC_name_all.objects.filter(idc_company=server_idc_company,idc_name=server_idc):
                re_server_id = IDC_name_all.objects.get(idc_company=server_idc_company,idc_name=server_idc).idc_scode + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id + '.' + server_id
            elif server_idc_company == u'其他':
                for idc in IDC_name_all.objects.all():
                    if not idc.idc_company and idc.idc_name == server_idc:
                        re_server_id = idc.idc_scode + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id + '.' + server_id
                if not re_server_id:
                    re_server_id = 'No' + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id + '.' + server_id
            else:
                re_server_id = 'No' + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id + '.' + server_id

            if Server_all.objects.filter(server_id=re_server_id):
                message = u'产品%s的服务器唯一id(%s)已经存在' %(server_product,server_id)
            else:
                if not server_start_date:
                    server_start_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                server_template = server_template.split("(")[0]
                server_hd = Server_template.objects.get(template_name=server_template)
                server_template_id = server_hd.id
                add_sql = Server_all(server_id=re_server_id,server_in_ip=server_in_ip,server_out_ip=server_out_ip,server_type=server_type,server_template_id=server_template_id,server_idc_company=server_idc_company,server_idc=server_idc,server_company=server_company,server_product=server_product,server_group=server_group,server_status=server_status,server_start_date=server_start_date)
                if add_sql:
                    try:
			event = "Add server Success with add one server operation, server id is %s" %server_id
			sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
			sql.save()
                        add_sql.save()
                        return HttpResponseRedirect('/cmdb')
                    except Exception,e:
                        message = e
    return render_to_response('cmdb/server_add.html',{'server_groups':server_groups,'companyall':companyall,'templateall':templateall,'typeall':typeall,'gameall':gameall,'idcall':idcall,'message':message,'server_line_status':server_status_list,'server_id':server_id,'server_in_ip':server_in_ip,'server_out_ip':server_out_ip,'server_type':server_type,'server_template':server_template,'server_idc_company':server_idc_company,'server_idc':server_idc,'server_company':server_company,'server_product':server_product,'server_group':server_group,'server_status':server_status,'server_start_date':server_start_date,'template_name':template_name,'company_list':company_list,'company_idc_dict':company_idc_dict,'default_idc':default_idc},context_instance=RequestContext(request))

#批量添加服务器
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.add_server') == True,login_url='/home/')
def server_many_add(request):
    mess = []
    server_ids = []
    error_many_list = [] 
    added_server_ids = ""
    in_ip_valid = True
    out_ip_valid = True
    regex=ur"((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)(:\d{1,})?$"
    if request.method == 'POST':
        #获取批量传过来的信息
        many_string = request.POST.get('many_server',None)
        if many_string != None:
            #以回车为分隔符进行分割
            for i in many_string.strip().split("\n"):
                start_date_valid = True
                #在以逗号为分隔符，得到一个列表
                one_server = i.strip().split(",")
                #列表长度定长为11
                if len(one_server) == 12:
                    #检查内网IP是否合法
                    if one_server[1]:
                        if not re.match(regex,one_server[1]):
                            in_ip_valid = False
                            message=u"提供的内网ip地址非法"
                    #检查外网IP是否合法
                    if one_server[2]:
                        if not re.match(regex,one_server[2]):
                            out_ip_valid = False
                            message=u"提供的外网ip地址非法"
                    if one_server[11]:
                        if len(one_server[11]) != 10:
                            start_date_valid = False
                        else:
                            start_date = one_server[11].split('-')
                            if len(start_date) != 3 or len(start_date[0]) != 4 or len(start_date[1]) != 2 or len(start_date[2]) != 2:
                                start_date_valid = False
                            else:
                                server_start_date = one_server[11]
                    else:
                        server_start_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                    if len(one_server[0].split('.')) != 2:
                        mess.append(u'%s服务器唯一标示不合法' %one_server[0])
                        error_many_list.append(i)
                    elif not in_ip_valid:
                        mess.append(u'服务器id为%s的内网IP地址非法' %one_server[0])
                        error_many_list.append(i)
                    elif not out_ip_valid:
                        mess.append(u'服务器id为%s的外网IP地址非法' %one_server[0])
                        error_many_list.append(i)
                    elif not Server_type_all.objects.filter(server_type_name=one_server[3]):
                        mess.append(u'%s主机类型%s不是云主机或者物理机' %(one_server[0],one_server[3]))
                        error_many_list.append(i)
                    elif not Server_template.objects.filter(template_name=one_server[4]):
                        mess.append(u'%s模板不在服务器模板中，请先添加模板' %(one_server[4]))
                        error_many_list.append(i)
                    elif one_server[5] and not IDC_name_all.objects.filter(idc_company=one_server[5]):
                        mess.append(u'%sIDC所属公司不在IDC列表中,请检查' %(one_server[5]))
                        error_many_list.append(i)
                    elif not IDC_name_all.objects.filter(idc_name=one_server[6]):
                        mess.append(u'服务器IDC%s不在列表中' %(one_server[6]))
                        error_many_list.append(i)
                    elif not Game_name_all.objects.filter(game_name=one_server[7]):
                        mess.append(u'服务器所属产品%s不在游戏列表中'%(one_server[7]))
                        error_many_list.append(i)
                    elif one_server[8] and one_server[8] not in server_groups:
                        mess.append(u'服务器所属组%s不在组列表中'%(one_server[8]))
                        error_many_list.append(i)
                    elif not Server_platform.objects.filter(platform_name=one_server[9]):
                        mess.append(u'%s平台不在平台列表中，请先添加平台' %(one_server[9]))
                        error_many_list.append(i)
                    elif one_server[10].title() not in server_status_list:
                        mess.append(u'服务器状态不能为%s'%(one_server[10]))
                        error_many_list.append(i)
                    elif not start_date_valid:
                        mess.append(u'时间%s为无效格式时间,格式为2013-01-01' %(one_server[11]))
                        error_many_list.append(i)
                    else:
                        temp_scode = ''
                        game_string_id = Game_name_all.objects.get(game_name=one_server[7]).game_string_id
                        if not one_server[5]:
                            for name in IDC_name_all.objects.all():
                                if (name.idc_company == None or name.idc_company == '') and name.idc_name == one_server[6]:
                                    temp_scode = name.idc_scode
                        else:
                            if IDC_name_all.objects.filter(idc_company=one_server[5],idc_name=one_server[6]):
                                temp_scode = IDC_name_all.objects.get(idc_company=one_server[5],idc_name=one_server[6]).idc_scode
                        if temp_scode == '':
                            temp_scode = 'No'
                        re_server_id = temp_scode + '.' + game_string_id + '.' + one_server[0]
                        if Server_all.objects.filter(server_id=re_server_id):
                            mess.append(u'产品为%s的服务器唯一标示%s已经存在' %(one_server[7],one_server[0]))
                            error_many_list.append(i)
                        template_message = Server_template.objects.get(template_name=one_server[4])
                        server_template_id = template_message.id
                        input_db = Server_all(server_id=re_server_id,server_in_ip=one_server[1],server_out_ip=one_server[2],server_type=one_server[3],server_template_id=server_template_id,server_idc_company=one_server[5],server_idc=one_server[6],server_company=one_server[9],server_product=one_server[7],server_group=one_server[8],server_status=one_server[10],server_start_date=server_start_date)
                        if input_db:
                            try:
				server_ids.append(one_server[0])
                                input_db.save()
                            except Exception,e:
                                message = e
                                error_many_list.append(i)
                else:
                    mess.append(u"%s添加失败，请检查添加项" %i)
                    error_many_list.append(i)
        else:
            mess.append(u"添加文本为空")
        for element in server_ids:
           added_server_ids = added_server_ids+' '+element
        if added_server_ids.strip():
           event="Add servers success with adding multiple servers, ids are%s" %added_server_ids
           sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
           sql.save()
    return render_to_response('cmdb/server_many_add.html',{'error_manage_list':error_many_list,'mess':mess},context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.add_server') == True,login_url='/home/')
def server_simplify_add(request):
    #
    server_id = ""
    server_in_ip = ""
    server_out_ip = ""
    company_idc_dict = {}
    company_list = []
    default_company = ''
    default_idc = []
    message = ''
    user_game_dict = {}
    success = False
    typeall = Server_type_all.objects.all()
    distinct_server_id = Server_all.objects.values("server_id").distinct()

    per_all = Permission.objects.all()
    user = str(request.user)
    if user == 'admin':
        gameall = Game_name_all.objects.all()
    else:
        for per in per_all:
            user_game_dict[per.codename] = per.name
        if user in user_game_dict:
            gameall = user_game_dict[user].split(" ")

    templateall = Server_template.objects.all()
    companyall = Server_platform.objects.all()
    idc_all_name = IDC_name_all.objects.all()
    game_dict = Game_name_all.objects.all()

    for name in idc_all_name:
        if name.idc_company == None or name.idc_company == '':
            company_name = u"其他"
        else:
            company_name = name.idc_company

        if not default_company or default_company == company_name:
            default_company = company_name
            default_idc.append(name.idc_name)

        if company_name not in company_list:
            company_list.append(company_name)
        if company_name not in company_idc_dict:
            company_idc_dict[company_name] = [name.idc_name]
        else:
            company_idc_dict[company_name] += [name.idc_name]

    if request.method == 'POST':
        start = 0
        temp_server_id = ''
        server_type = request.POST.get('server_type',None)
        server_template = request.POST.get('server_template',None)
        server_idc_company = request.POST.get('idc_company',None)
        server_idc = request.POST.get('server_idc',None)
        server_company = request.POST.get('server_company',None)
        server_product = request.POST.get('server_product',None)
        server_status = request.POST.get('server_status',None)
        server_start_date = request.POST.get('server_start_date',None)
        if not server_start_date:
            server_start_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        if IDC_name_all.objects.filter(idc_company=server_idc_company,idc_name=server_idc):
            temp_server_id = IDC_name_all.objects.get(idc_company=server_idc_company,idc_name=server_idc).idc_scode + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id
        elif server_idc_company == u"其他":
            for name in idc_all_name:
                if (name.idc_company == None or name.idc_company == '') and name.idc_name == server_idc:
                    temp_server_id = name.idc_scode + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id
            if not temp_server_id:
                temp_server_id = 'No' + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id
        else:
            temp_server_id = 'No' + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id

        for i in range(50):
            re_server_id = ''
            Found = False
            loop_times = 0
            while loop_times < 50 and not Found:
                server_id = request.POST.get("server_ids"+str(start), "")
                server_in_ip = request.POST.get("server_in_ips"+str(start), "")
                server_out_ip = request.POST.get("server_out_ips"+str(start), "")
                if server_id:
                    Found = True
                    re_server_id = temp_server_id + '.' + server_id
                start += 1
                loop_times += 1
            if server_id and (server_in_ip or server_out_ip):
                server_template_id = Server_template.objects.get(template_name=server_template).id
                sql = Server_all(server_id=re_server_id,server_in_ip=server_in_ip,server_out_ip=server_out_ip,server_type=server_type,server_template_id=server_template_id,server_idc_company=server_idc_company,server_idc=server_idc,server_company=server_company,server_product=server_product,server_status=server_status,server_start_date=server_start_date)
                sql.save()
                success = True
            elif server_id and not (server_in_ip or server_out_ip):
                message += server_id + '/'
    if success and not message:
        return HttpResponseRedirect('/cmdb')
    return render_to_response('cmdb/server_simplify_add.html',{'message':message,'typeall':typeall,'gameall':gameall,'game_dict':game_dict,'distinct_server_id':distinct_server_id,'templateall':templateall,'companyall':companyall,'company_list':company_list,'idc_all_name':idc_all_name,'company_idc_dict':company_idc_dict,'default_idc':default_idc,'server_line_status':server_status_list},context_instance=RequestContext(request))

#服务器删除函数
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.server_del') == True,login_url='/home/')
def server_del(request):
    message = []
    server_ids = []
    deleted_server_ids = ""
    error = ''
    content = ''
    #定义个默认值
    field = u'主机类型'
    check_content = ''
    object_admin = Game_name_all.objects.all()
    if request.method == 'GET':
        page_num = request.GET.get('page',1)
        if page_num != "all":
            page_num = int(page_num)
        server_field = request.GET.get('server_field',None)
        if server_field == None or server_field == '':
            field = field
        else:
            field = server_field
        search_field = variable_db_dict[field]
        check_content = request.GET.get('many_message',None)
        content = server_search(search_field,check_content)
        #分页
        page_v = int(ceil(len(content)/page_value))
        page_list = [ x+1 for x in range(page_v) ]
        page_start_end,page_up,page_next,first_page,last_page,last_page_value = pagination(page_list,page_num)
        #分页数据提取
        if page_num == 'all':
            content = content
        else:
            if page_num == int(last_page_value):
                start_value = (page_num - 1) * int(page_value)
                content = content[start_value::]
            elif page_num == int(first_page):
                end_value = int(page_value)
                content = content[0:end_value]
            else:
                start_value = (page_num - 1) * int(page_value)
                end_value = page_num * int(page_value)
                content = content[start_value:end_value]
        id_list = request.GET.getlist('check_box')
        if len(id_list) != 0:
            for s_id in id_list:
                server_information = Server_all.objects.get(id=s_id)
                if server_information:
                    try:
                        server_information.delete()
                        message.append(u"%s删除success" %server_information.server_id)
			server_ids.append(server_information.server_id)
                    except Exception,e:
                        error = e
	for element in server_ids:
		deleted_server_ids = deleted_server_ids + ' ' + element
	if deleted_server_ids:
		event='Delete servers success with delete multiple servers, ids are %s' %deleted_server_ids
		sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
		sql.save()
    return render_to_response("cmdb/server_del.html",{'page_num':page_num,'page_list':page_start_end,'page_up':page_up,'page_next':page_next,'first_page':first_page,'last_page':last_page,'last_page_value':last_page_value,'object_admin':object_admin,'server_field':field,'check_content':check_content,'variable_db':variable_db_dict,'check_server':content,'message':message},context_instance=RequestContext(request))

#单台机器删除
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def one_server_del(request,offset,product):
    offset = int(offset)
    product1= u"修改"+product
    user = User.objects.get(username=request.user)
    server_information = Server_all.objects.get(id=offset)
    message = ''
    per = permission_auth(request.user,product)
    if per == False:
        return HttpResponseRedirect("/home")
    else:
        if request.method == "POST":
            try:
                server_information.delete()
                message = u"%s删除success" %server_information
		event='Delete server success with delete only one server, id is %s' %server_information.server_id
		sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
		sql.save()
            except Exception,e:
                message = e
    return render_to_response("cmdb/one_server_del.html",{'server_information':server_information,'message':message},context_instance=RequestContext(request))

#服务器编辑
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home/')
def server_edit(request,offset,product):
    per = permission_auth(request.user,product)
    if per == False:
        return HttpResponseRedirect("/home")
    else:
        message = ''
        gameall = {}
        company_list = []
        company_idc_dict = {}
        default_idc = []
        user_game_dict = {}
        start_date_valid = True
        end_date_valid = True
        idcall = IDC_name_all.objects.filter()
        per_all = Permission.objects.all()
        user = str(request.user)
        if user == 'admin':
            gameall = Game_name_all.objects.all()
        else:
            for per in per_all:
                user_game_dict[per.codename] = per.name
            if user in user_game_dict:
                gameall = user_game_dict[user].split(" ")
        typeall = Server_type_all.objects.all()
        templateall = Server_template.objects.all()
        companyall = Server_platform.objects.all()
        offset = int(offset)
        s_edit = Server_all.objects.get(id__exact=offset)
        s_id = s_edit.server_id

        default_company = s_edit.server_idc_company
        idc_all_name = IDC_name_all.objects.all()
        for name in idc_all_name:
            if name.idc_company == None or name.idc_company == '':
                company_name = u"其他"
            else:
                company_name = name.idc_company

            if default_company == company_name:
                default_idc.append(name.idc_name)

            if company_name not in company_list:
                company_list.append(company_name)
            if company_name not in company_idc_dict:
                company_idc_dict[company_name] = [name.idc_name]
            else:
                company_idc_dict[company_name] += [name.idc_name]

        if request.method == "POST":
            id = int(offset)
            server_id = request.POST.get('server_id',None)
            server_in_ip = request.POST.get('server_in_ip',None)
            server_out_ip = request.POST.get('server_out_ip',None)
            server_type = request.POST.get('server_type',None)
            server_template = request.POST.get('server_template',None)
            server_idc_company = request.POST.get('idc_company',None)
            server_idc = request.POST.get('server_idc',None)
            server_company = request.POST.get('server_company',None)
            server_product = request.POST.get('server_product',None)
            server_group = request.POST.get('server_group',None)
            server_status = request.POST.get('server_status',None)
            server_start_date = request.POST.get('server_start_date','')
            server_end_date = request.POST.get('server_end_date','')
            if server_start_date:
                if len(server_start_date) != 10:
                    start_date_valid = False
                start_date = server_start_date.split('-')
                if len(start_date) != 3 or len(start_date[0]) != 4 or len(start_date[1]) != 2 or len(start_date[2]) != 2:
                    start_date_valid = False
            else:
                start_date_valid = False
            if server_end_date:
                if len(server_end_date) != 10:
                    end_date_valid = False
                end_date = server_end_date.split('-')
                if len(end_date) != 3 or len(end_date[0]) != 4 or len(end_date[1]) != 2 or len(end_date[2]) != 2:
                    end_date_valid = False
            if server_id == None or server_id == '':
                message = u"服务器唯一id信息不能为空"
            elif len(server_id.split('.')) != 2:
                message = u"服务器唯一id信息无效,正确格式为:game.s5"
            elif server_type == None or server_type == '':
                message = u"主机类型信息不能为空"
            elif server_idc == None or server_idc == '':
                message = u"服务器机房信息不能为空"
            elif server_company == None or server_company == '':
                message = u"服务器公司信息不能为空"
            elif server_status == None or server_status == '':
                message = u"服务器状态信息不能为空"
            elif not start_date_valid:
                message = u"服务器开始时间无效"
                if not server_start_date:
                    message = u"服务器开始时间不能为空"
            elif not end_date_valid:
                message = u"服务器结束时间无效"
            else:
                re_server_id = ''
                server_template = server_template.split("(")[0]
                server_hd = Server_template.objects.get(template_name=server_template)
                server_template_id = server_hd.id
                if IDC_name_all.objects.filter(idc_company=server_idc_company,idc_name=server_idc):
                    re_server_id = IDC_name_all.objects.get(idc_company=server_idc_company,idc_name=server_idc).idc_scode + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id + '.' + server_id
                elif server_idc_company == u'其他':
                    for idc in IDC_name_all.objects.all():
                        if (idc.idc_company == None or idc.idc_company == '') and idc.idc_name == server_idc:
                            re_server_id = idc.idc_scode + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id + '.' + server_id
                    if not re_server_id:
                        re_server_id = 'No' + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id + '.' + server_id
                else:
                    re_server_id = 'No' + '.' + Game_name_all.objects.get(game_name=server_product).game_string_id + '.' + server_id
                  
                if s_id != re_server_id:
                    if Server_all.objects.filter(server_id=re_server_id):
                        message = u'产品%s的服务器唯一id(%s)已经存在' %(server_product,server_id)
                    else:
                        if Server_all.objects.filter(id__exact=id).update(server_id=re_server_id,server_in_ip=server_in_ip,server_out_ip=server_out_ip,server_type=server_type,server_template_id=server_template_id,server_idc_company=server_idc_company,server_idc=server_idc,server_company=server_company,server_product=server_product,server_group=server_group,server_status=server_status,server_start_date=server_start_date,server_end_date=server_end_date):
                            message = u"%s修改成功" %server_id
                            event='Edit server success, id is %s' %server_id
                            sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                            sql.save()
                            return HttpResponseRedirect('/cmdb/server_product=%s' %server_product)
                else:
                    if Server_all.objects.filter(id__exact=id).update(server_id=re_server_id,server_in_ip=server_in_ip,server_out_ip=server_out_ip,server_type=server_type,server_template_id=server_template_id,server_idc_company=server_idc_company,server_idc=server_idc,server_company=server_company,server_product=server_product,server_group=server_group,server_status=server_status,server_start_date=server_start_date,server_end_date=server_end_date):
                        message = u"%s修改成功" %server_id
                        event='Edit server success, id is %s' %server_id
                        sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                        sql.save()
                        return HttpResponseRedirect('/cmdb/server_product=%s' %server_product)
    return render_to_response("cmdb/server_edit.html",{'server_template_dict':server_template_dict,'companyall':companyall,'templateall':templateall,'typeall':typeall,'message':message,'s_edit':s_edit,'idcall':idcall,'gameall':gameall,'server_line_status':server_status_list,'company_list':company_list,'default_idc':default_idc,'company_idc_dict':company_idc_dict,'server_groups':server_groups},context_instance=RequestContext(request))


#IDC管理
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_idc') == True,login_url='/home')
def idc_all(request):
    company_idc_mess_dict = {}
    company_list = []
    if request.method == "GET":
        idc_all_name = IDC_name_all.objects.all()
        for name in idc_all_name:
            if name.idc_company == None or name.idc_company == '':
                company_name = u"其他"
            else:
                company_name = name.idc_company
            if company_name not in company_list:
                if company_name == "HL":
                    company_list.insert(0,company_name)
                else:
                    company_list.append(company_name)
            if company_name not in company_idc_mess_dict:
                company_idc_mess_dict[company_name] = [name]
            else:
                company_idc_mess_dict[company_name] += [name]
    return render_to_response('cmdb/idc_all.html',{'company_list':company_list,'idc_all_name':company_idc_mess_dict},context_instance=RequestContext(request))


#主机内型管理
#@login_required
#@user_passes_test(lambda u:u.has_perm('hlcmdb.see_idc_num') == True,login_url='/home')
#def server_type_all(request):
#    if request.method == "GET":
#        type_all_name = Server_type_all.objects.all()
#        all_type_count = type_all_name.count()
#    return render_to_response('cmdb/server_type_all.html',{'type_all_name':type_all_name,'all_type_count':all_type_count},context_instance=RequestContext(request))
#
#IDC添加
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.add_idc') == True,login_url='/home')
def idc_add(request):
    idc_company = ''
    idc_name = ''
    idc_address = ''
    idc_contact = ''
    idc_phone = ''
    idc_scode = ''
    message = ''
    if request.method == "POST":
        idc_company = request.POST.get('idc_company',None)
        idc_name = request.POST.get('idc_name',None)
        idc_scode = request.POST.get('idc_scode',None)
        idc_address = request.POST.get('idc_address',None)
        idc_contact = request.POST.get('idc_contact',None)
        idc_phone = request.POST.get('idc_phone',None)
        if idc_name == None or idc_name == '':
            message = u"请输入idc名称"
        elif IDC_name_all.objects.filter(idc_company=idc_company,idc_name=idc_name):
	        message = u'idc名称%s已经存在' %idc_name
	else:
            idc = IDC_name_all(idc_company=idc_company,idc_name=idc_name,idc_address=idc_address,idc_scode=idc_scode,idc_contact=idc_contact,idc_phone=idc_phone)
            if idc:
                try:
                    idc.save()
                    message = u'IDC:%s添加success' %idc_name
                    event='Add IDC success, IDC name is %s' %idc_name
                    sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                    sql.save()
                except Exception,e:
                    message = e
    return render_to_response('cmdb/idc_add.html',{'idc_company':idc_company,'idc_name':idc_name,'idc_address':idc_address,'idc_scode':idc_scode,'idc_contact':idc_contact,'idc_phone':idc_phone,'message':message},context_instance=RequestContext(request))

#IDC编辑
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.add_idc') == True,login_url='/home')
def idc_edit(request,offset):
    message = ''
    id = int(offset)
    idc_message = IDC_name_all.objects.get(id__exact=id)
    old_idc_name = idc_message.idc_name
    if request.method == "POST":
        idc_company = request.POST.get('idc_company',None)
        idc_name = request.POST.get('idc_name',None)
        idc_scode = request.POST.get('idc_scode',None)
        idc_address = request.POST.get('idc_address',None)
        idc_contact = request.POST.get('idc_contact',None)
        idc_phone = request.POST.get('idc_phone',None)
        if idc_name == '' or idc_name == None:
            message = u"IDC名称不能为空"
        else:
            if idc_name != old_idc_name:
                if IDC_name_all.objects.filter(idc_company=idc_company,idc_name=idc_name):
                    message = u"IDC已经存在"
                else:
                    edit_idc = IDC_name_all.objects.filter(id__exact=id).update(idc_company=idc_company,idc_name=idc_name,idc_scode=idc_scode,idc_address=idc_address,idc_contact=idc_contact,idc_phone=idc_phone)
                    if edit_idc:
                        event='Edit IDC success, IDC name is %s' %idc_name
                        sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                        sql.save()
                        return HttpResponseRedirect('/cmdb/idc_all') 
            else:
                edit_idc = IDC_name_all.objects.filter(id__exact=id).update(idc_company=idc_company,idc_name=idc_name,idc_scode=idc_scode,idc_address=idc_address,idc_contact=idc_contact,idc_phone=idc_phone)
                if edit_idc:
                    event='Edit IDC success, IDC name is %s' %idc_name
                    sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                    sql.save()
                    return HttpResponseRedirect('/cmdb/idc_all') 
    return render_to_response('cmdb/idc_edit.html',{'idc_message':idc_message,'message':message},context_instance=RequestContext(request))

#游戏名管理函数
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_game') == True,login_url='/home')
def game_all(request):
    game_type_name = Game_type_name.objects.all()
    game_all_name = Game_name_all.objects.all()
    if request.method == "GET":
        game_type = request.GET.get('game_type_name',"all")
        if game_type == "all":
            game_all_name = game_all_name
        else:
            game_all_name = Game_name_all.objects.filter(game_type=game_type)
        all_game_count = game_all_name.count()
        page_num = request.GET.get('page',1)
        if page_num != 'all':
            page_num = int(page_num)
        page_start_end,page_up,page_next,first_page,last_page,page_all_data,last_page_value = pagination_django(game_all_name,page_value,page_num)
    return render_to_response('cmdb/game_all.html',{'game_type_name':game_type_name,'game_type':game_type,'page_num':page_num,'last_page_value':last_page_value,'game_all_name':page_all_data,'page_list':page_start_end,'page_up':page_up,'page_next':page_next,'first_page':first_page,'last_page':last_page},context_instance=RequestContext(request)) 

#游戏名添加函数
import string
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.add_game') == True,login_url='/home')
def game_add(request):
    game_name = ''
    game_appid = ''
    user_name = ''
    oper_models = ''
    user_phone = ''
    yunying_name = ''
    yunying_phone = ''
    developer_name = ''
    developer_phone = ''
    game_line = ''
    special_list = []
    game_type_name = Game_type_name.objects.all()
    special_string = string.punctuation + "（）【】"
    message = ''
    game_platform = ''
    game_type = ''
    if request.method == "POST":
        game_type = request.POST.get('game_type',None)
        game_name = request.POST.get('game_name',None)
        game_appid = request.POST.get('game_appid',None)
        oper_models = request.POST.get('oper_models',None)
        user_name = request.POST.get('user_name',None)
        user_phone = request.POST.get('user_phone',None)
        yunying_name = request.POST.get('yunying_name',None)
        yunying_phone = request.POST.get('yunying_phone',None)
        developer_name = request.POST.get('developer_name',None)
        developer_phone = request.POST.get('developer_phone',None)
        game_line = request.POST.get('game_line',None)
        if game_name == None or game_name == '':
            message = u"请输入要添加的游戏名"
        elif Game_name_all.objects.filter(game_name=game_name):
            message = u"%s游戏名已经存在" %game_name
        else:
            for s in game_name:
                if s.encode("utf8") in special_string:
                    special_list.append(s)
            if len(special_list) != 0:
                s_s = ''
                for i in special_list:
                    s_s += i
                message = u'游戏名中有特殊字符' + s_s
            else:
                game_add = Game_name_all(game_type=game_type,game_name=game_name,game_appid=game_appid,oper_models=oper_models,user_name=user_name,user_phone=user_phone,yunying_name=yunying_name,yunying_phone=yunying_phone,developer_name=developer_name,developer_phone=developer_phone,game_line=game_line)
                if game_add:
                    try:
                        game_add.save()
                        gamename_message = Game_name_all.objects.filter(game_name__exact=game_name)
                        for g in gamename_message:
                            id = str(g.id)
                        if len(id) < 3:
                            num = 3 - len(id)
                            game_string_id = 'hl'+'0'*num+id
                        else:
                            game_string_id = 'hl'+id
                        Game_name_all.objects.filter(game_name__exact=game_name).update(game_string_id=game_string_id)
                        message = u"game:%s添加success" %game_name
                        event=u'添加游戏成功,游戏名称是%s' %game_name
                        sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                        sql.save()
                        if not request.user.is_staff:
                            all_per_game = Permission.objects.get(codename=request.user).name
                            all_per_game = all_per_game + " " + game_name
                            Permission.objects.filter(codename=request.user).update(name=all_per_game)
                    except Exception,e:
                        message = e
    return render_to_response('cmdb/game_add.html',{'game_line':game_line,'oper_model':oper_models,'game_type_name':game_type_name,'oper_models':operation_models,'message':message,'game_line_status':server_status_list,'game_platform':game_type,'game_name':game_name,'game_appid':game_appid,'user_name':user_name,'user_phone':user_phone,'yunying_name':yunying_name,'yunying_phone':yunying_phone,'developer_name':developer_name,'developer_phone':developer_phone},context_instance=RequestContext(request))

#游戏编辑
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.add_game') == True,login_url='/home')
def game_edit(request,offset):
    message = ''
    game_id = int(offset)
    game_type_all = Game_type_name.objects.all()
    g_edit = Game_name_all.objects.get(id__exact=game_id)
    g_name = g_edit.game_name
    per = permission_auth(request.user,g_name)
    if per == False:
        return HttpResponseRedirect("/home")
    else:
        if request.method == "POST":
            g_edit = game_id
            id = str(game_id)
            if len(id) < 3:
                num = 3 - len(id)
                game_string_id = 'hl'+'0'*num+id
            else:
                game_string_id = 'hl'+id
            game_type = request.POST.get('game_type')
            game_name = request.POST.get('game_name',None)
            game_appid = request.POST.get('game_appid',None)
            oper_models = request.POST.get('oper_models',None)
            user_name = request.POST.get('user_name',None)
            user_phone = request.POST.get('user_phone',None)
            yunying_name = request.POST.get('yunying_name',None)
            yunying_phone = request.POST.get('yunying_phone',None)
            backup_yunying_name = request.POST.get('backup_yunying_name',None)
            backup_yunying_phone = request.POST.get('backup_yunying_phone',None)
            developer_name = request.POST.get('developer_name',None)
            developer_phone = request.POST.get('developer_phone',None)
            backup_developer_name = request.POST.get('backup_developer_name',None)
            backup_developer_phone = request.POST.get('backup_developer_phone',None)
            game_line = request.POST.get('game_line',None)
            if game_name == None or game_name == '':
                message = u"游戏名称不能为空"
            elif game_line == None or game_line == '':
                message = u"游戏状态不能为空"
            else:
                if g_name != game_name:
                    if Game_name_all.objects.filter(game_name=game_name):
                        message = u"游戏名已经存在"
                    else:
                        try:
                            add_game = Game_name_all.objects.filter(id__exact=game_id).update(game_type=game_type,game_name=game_name,oper_models=oper_models,game_appid=game_appid,game_string_id=game_string_id,user_name=user_name,user_phone=user_phone,yunying_name=yunying_name,yunying_phone=yunying_phone,backup_yungying_name=backup_yunying_name,backup_yunying_phone=backup_yunying_phone,developer_name=developer_name,developer_phone=developer_phone,backup_developer_name=backup_developer_name,backup_developer_phone=backup_developer_phone,game_line=game_line)
                            if add_game:
                                event=u'编辑游戏成功，游戏名称被改变，原名称是%s，新名称是%s' %(g_name,game_name)
                                sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                                sql.save()
                                return HttpResponseRedirect('/cmdb/game_all/')
                        except Exception,e:
                            message = e
                else:
                    try:
                        add_game = Game_name_all.objects.filter(id__exact=game_id).update(game_type=game_type,game_name=game_name,oper_models=oper_models,game_appid=game_appid,game_string_id=game_string_id,user_name=user_name,user_phone=user_phone,yunying_name=yunying_name,yunying_phone=yunying_phone,backup_yunying_name=backup_yunying_name,backup_yunying_phone=backup_yunying_phone,developer_name=developer_name,developer_phone=developer_phone,backup_developer_name=backup_developer_name,backup_developer_phone=backup_developer_phone,game_line=game_line)
                        if add_game:
                            event=u'编辑游戏成功，游戏名称未被改变，名称是%s' %game_name
                            sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                            sql.save()
                            return HttpResponseRedirect('/cmdb/game_all/')
                    except Exception,e:
                        message = e
    return render_to_response('cmdb/game_edit.html',{'game_type_all':game_type_all,'oper_models':operation_models,'game_status':server_status_list,'message':message,'game_line_status':server_status_list,"g_edit":g_edit},context_instance=RequestContext(request))


#组用户管理函数
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_user') == True,login_url='/home')
def user_all(request):
    group_user = {}
    if request.method == "GET":
        user_group_data = Group.objects.all()
        for group in user_group_data:
            user = group.user_set.all()
            if len(user) == 0:
                group_user[group] = [None]
            else:
                for user in user:
                    if group not in group_user:
                        group_user[group] = [user]
                    else:
                        group_user[group] += [user]
    return render_to_response('cmdb/user_all.html',{'group_user':group_user},context_instance=RequestContext(request))

#用户添加
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.user_add') == True,login_url='/home')
def user_add(request):
    message = ''
    groupall = Group.objects.all()
    if request.method == "POST":
        user = request.POST.get('user_name',None)
        passwd = request.POST.get('password',None)
        user_group = request.POST.get('user_group',None)
        check_list = request.POST.getlist('check_box',None)
        if user == None or passwd == None or user_group == None or user == '' or passwd == '' or user_group =='':
            message = u'用户名或密码不能为空'
        else:
            c_user = User.objects.filter(username=user)
            if c_user:
                message = u'用户已经存在'
            else:
                if len(passwd) < 6:
                    message = u'密码小于6位'
                else:
                    u = User.objects.create(username=user)
                    if u:
                        try:
                            u.set_password(passwd)
                            u.save()
                            event = u'添加用户成功，用户名是%s' %user
                            sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                            sql.save()
                            g = Group.objects.get(name=user_group)
                            if g:
                                u.groups.add(g)
                                message = u'%s用户添加成功，属组%s' %(user,user_group)
                            if not Permission.objects.filter(codename=user):
                                per_add = Permission(codename=user,content_type_id=7)
                                if per_add:
                                    per_add.save()
                                    per = Permission.objects.get(codename=user)
                                    u.user_permissions.add(per)
                            else:
                                per = Permission.objects.get(codename=user)
                                u.user_permissions.add(per)
                        except Exception,e:
                            message = e
    return render_to_response("cmdb/user_add.html",{'groupall':groupall,'message':message},context_instance=RequestContext(request))

@login_required
def server_group(request):
    server_groups = Server_game_group.objects.all()
    return render_to_response("cmdb/server_group.html",{'server_groups':server_groups},context_instance=RequestContext(request))

@login_required
def server_group_add(request):
    message = ''
    if request.method == 'POST':
        server_group = request.POST.get('server_group', None)
        if server_group == '' or server_group == None:
            message = u'服务器组名不能为空'
        elif Server_game_group.objects.filter(group_name=server_group):
            message = u'服务器组名已经存在'
        else:
            sql = Server_game_group(group_name=server_group)
            sql.save()
    return render_to_response("cmdb/server_group_add.html",{'message':message},context_instance=RequestContext(request))
#登出函数
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")

#使用说明
@login_required
def direction(request):
    return render_to_response("cmdb/direction.html",{},context_instance=RequestContext(request))

#为其他用户重置密码
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.user_add') == True,login_url='/home')
def reset_password_for_other_user(request):
    message = ''
    user_name = ''
    if request.method == "POST":
        user_name = request.POST.get('user_name',None)
        newpasswd = request.POST.get('user_new_passwd',None)
        true_passwd = request.POST.get('user_new_true',None)
        if User.objects.filter(username=user_name):
	    check_user = User.objects.get(username=user_name)
            if newpasswd != true_passwd:
                message = u'2次输入的密码不匹配'
            else:
                if len(newpasswd) >= 6:
                    try:
                        check_user.set_password(newpasswd)
                        check_user.save()
                        message = u'重置密码成功'
                    except Exception,e:
                        message = e
                else:
                    message = u"newpasswd小于6位"
        else:
            message =u'需要重置密码的用户名不存在'
    return render_to_response('cmdb/reset_password_for_other_user.html',{'username':user_name,'message':message},context_instance=RequestContext(request))
