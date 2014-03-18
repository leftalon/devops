#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2013-11-16 14:50:40'
__licence__	= 'GPL licence'

#import models
from django.contrib.auth.models import User,Group,Permission

#defined variable
codename_name_dict = {}
name_codename_dict = {}
def permission_auth(user,product):
    product = product
    user_login = unicode(user)
    user_per = User.objects.get(username=user)
    permission_all = Permission.objects.all()
    for p in permission_all:
        if p.codename not in codename_name_dict:
            codename_name_dict[p.codename] = p.name
    for k,v in codename_name_dict.items():
        p_list = v.split()
        for p in p_list:
            if p not in name_codename_dict:
                name_codename_dict[p] = k
    if product in name_codename_dict:
        u = name_codename_dict[product]
        per = u"hlcmdb."+u
    else:
        per = "no"
    return user.has_perm(per)
