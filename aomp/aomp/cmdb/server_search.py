#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2013-10-26 15:02:11'
__licence__	= 'GPL licence'

#import module
from django.db.models import Q
from aomp.cmdb.models import Server_all
from aomp.cmdb.variable_db import variable_db_dict

def server_search(field,message_content):
    Q_result = None
    kargs = {}
    field = field
    if message_content:
        kargs[field + "__exact"] = message_content
        Q_result = Q(**kargs)
    else:
        kargs[field + "__exact"] = 'none'
        Q_result = Q(**kargs)
    if Q_result:
        result = Server_all.objects.filter(Q_result)
    return result

def server_search_dict(**kargs):
    Q_result = None
    if kargs:
        Q_result = Q(**kargs)
        if Q_result:
            result = Server_all.objects.filter(Q_result)
    return result

def fan_search(message):
    Q_result = None
    if message:
        Q_r = Server_all.objects.filter(Q(server_id__icontains=message) | Q(server_in_ip__icontains=message) | Q(server_out_ip__icontains=message) | Q(server_template_id__icontains=message) | Q(server_company__icontains=message) | Q(server_product__icontains=message) | Q(server_status__icontains=message) | Q(server_idc__icontains=message))
    else:
        Q_r = Server_all.objects.filter(server_id='none')
    return Q_r
