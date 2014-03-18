#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2014-01-12 15:34:38'
__licence__	= 'GPL licence'

from hlcmdb.models import Server_template

def server_template_dict():
    global template_all_dict
    template_all_dict = {}
    template_all = Server_template.objects.all()
    for template_name in template_all:
        t_id = int(template_name.id)
        t_n = template_name.template_name
        t_model = template_name.template_model
        t_cpu = template_name.template_cpu
        t_mem = template_name.template_mem
        t_disk = template_name.template_disk
        if t_id not in template_all_dict:
            template_all_dict[t_id] = [t_n,t_model,t_cpu,t_mem,t_disk]
    return template_all_dict

def server_template_price():
    global server_template_id_price
    server_template_id_price = {}
    template_all = Server_template.objects.all()
    for template_id.id in template_all:
        if template_id not in server_template_id_price:
            server_template_id_price[template_id.id] = [template_id.template_name,template_template_money]
    return server_template_id_price
