#!/usr/bin/python
# encoding: utf-8

from aomp.cmdb.models import Server_all
from aomp.cmdb.models import Game_name_all
from aomp.cmdb.models import Server_platform
from aomp.cmdb.models import IDC_name_all,Server_type_all,Server_game_group
from aomp.cmdb.models import Event_record
from aomp.cmdb.server_status import server_status_list
from aomp.cmdb.operation_models import operation_models
from aomp.cmdb.models import Server_template
from aomp.cmdb.models import Game_type_name
from aomp.cmdb.server_template_dict import server_template_dict
import time,datetime
import re

def add_many_server(one_server):
    print one_server
    message = ''
    regex=ur"((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)(:\d{1,})?$"
    in_ip_valid = True
    out_ip_valid = True
    start_date_valid = True
    #检查内网IP是否合法
    if one_server[1]:
        if not re.match(regex,one_server[1]):
            in_ip_valid = False
            message = u"提供的内网ip地址非法"
    #检查外网IP是否合法
    if one_server[2]:
        if not re.match(regex,one_server[2]):
            out_ip_valid = False
            message = u"提供的外网ip地址非法"
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
        message = u'%s服务器唯一标示不合法' %one_server[0]
    elif not in_ip_valid:
        message = u'服务器id为%s的内网IP地址非法' %one_server[0]
    elif not out_ip_valid:
        message = u'服务器id为%s的外网IP地址非法' %one_server[0]
    elif not Server_type_all.objects.filter(server_type_name=one_server[3]):
        message = u'%s主机类型%s不是云主机或者物理机' %(one_server[0],one_server[3])
    elif not Server_template.objects.filter(template_name=one_server[4]):
        message = u'%s模板不在服务器模板中，请先添加模板' %(one_server[4])
    elif not IDC_name_all.objects.filter(idc_company=one_server[5]):
        message = u'%sIDC所属公司不在IDC列表中,请检查' %(one_server[5])
    elif not IDC_name_all.objects.filter(idc_name=one_server[6]):
        message = u'服务器IDC%s不在列表中' %(one_server[6])
    elif not Server_platform.objects.filter(platform_name=one_server[7]):
        message = u'%s平台不在平台列表中，请先添加平台' %(one_server[7])
    elif not Game_name_all.objects.filter(game_name=one_server[8]):
        message = u'服务器所属产品%s不在游戏列表中' %(one_serve[8])
    elif not Server_game_group.objects.filter(group_name=one_server[9]):
        message = u'服务器所属组%s不在组列表中' %(one_server[9])
    elif one_server[10].title() not in server_status_list:
        message = u'服务器状态不能为%s'%(one_server[10])
    elif not start_date_valid:
        message = u'时间%s为无效格式时间,格式为2013-01-01' %(one_server[11])
    else:
        temp_scode = ''
        game_string_id = Game_name_all.objects.get(game_name=one_server[8]).game_string_id
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
            message = u'产品为%s的服务器唯一标示%s已经存在' %(one_server[7],one_server[0])
        template_message = Server_template.objects.get(template_name=one_server[4])
        server_template_id = template_message.id
        input_db = Server_all(server_id=re_server_id,server_in_ip=one_server[1],server_out_ip=one_server[2],server_type=one_server[3],server_template_id=server_template_id,server_idc_company=one_server[5],server_idc=one_server[6],server_company=one_server[7],server_product=one_server[8],server_group=one_server[9],server_status=one_server[10],server_start_date=server_start_date)
        if input_db:
            try:
                input_db.save()
            except Exception,e:
                message = e
    return message
