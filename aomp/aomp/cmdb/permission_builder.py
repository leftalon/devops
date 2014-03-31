#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2013-11-15 09:30:16'
__licence__	= 'GPL licence'

#import models
from aomp.cmdb.models import Game_name_all
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext
from django.contrib.auth.models import Permission
#defined variable
username_hanzi_spell= {
                    u'aaaa':'aaaa'}

#生成一个权限表，然后刷新的时候导入数据库进行权限变更
@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.add_user') == True,login_url='/home')
def permission_table(request):
    user_permission_list = []
    user_permission_dict = {}
    game_all = Game_name_all.objects.all()
    for game in game_all:
        game_permission = game.game_name
        game_user = game.user_name
        if game_user in username_hanzi_spell:
            user_key = username_hanzi_spell[game_user]
            if user_key in user_permission_dict:
                user_permission_dict[user_key] += game_permission + " "
            else:
                user_permission_dict[user_key] = game_permission + " "
        else:
            if game_user in user_permission_dict:
                user_permission_dict[game_user] += game_permission + " "
            else:
                user_permission_dict[game_user] = game_permission + " "
    for k,v in user_permission_dict.items():
        user_permission_list.append((k,v))
    if request.method == "POST":
        many_per = request.POST.get("many_per",None)
        one_per = many_per.split(";")
        for per in one_per:
            per = per.strip().split(":")
            if len(per) == 2:
                codename = per[0]
                name = per[1]
                Permission.objects.filter(codename=codename).update(name=name)
    return render_to_response("cmdb/permission_builder.html",{'user_permission_list':user_permission_list},context_instance=RequestContext(request))
