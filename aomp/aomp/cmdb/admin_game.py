#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2013-11-04 18:19:41'
__licence__	= 'GPL licence'

from django.shortcuts import render_to_response
from aomp.cmdb.models import Server_all
from aomp.cmdb.models import Game_name_all
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext

#项目管理对应表
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def admin_game(request):
    all_information = {}
    #得到所有game name表中的数据
    people_information = Game_name_all.objects.all()
    for people_one in people_information:
            product_name = people_one.game_name
            oper_models = people_one.oper_models
            people_name = people_one.user_name
            people_phone = people_one.user_phone
            yunying_name = people_one.yunying_name
            yunying_phone = people_one.yunying_phone
            #实际服务器的台数
            product_num = Server_all.objects.filter(server_product__exact=product_name).values("server_in_ip","server_out_ip").distinct().count()
            #以管理员的名字为key，其他的所有数据为value
            if people_name not in all_information:
                all_information[people_name] = [[people_phone,product_name,oper_models,yunying_name,yunying_phone,product_num]]
            else:
                all_information[people_name] += [[people_phone,product_name,oper_models,yunying_name,yunying_phone,product_num]]
    return render_to_response("cmdb/admin_game.html",{'all_information':all_information},context_instance=RequestContext(request))
