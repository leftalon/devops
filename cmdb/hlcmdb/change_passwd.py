#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2013-11-12 14:22:30'
__licence__	= 'GPL licence'

#import module
from django.contrib.auth.admin import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def change_passwd(request):
    message = ''
    user = request.user
    if request.method == "POST":
        passwd = request.POST.get('user_old_passwd',None)
        newpasswd = request.POST.get('user_new_passwd',None)
        true_passwd = request.POST.get('user_new_true',None)
        check_user = User.objects.get(username=user)
        if check_user:
            password = check_user.check_password(passwd)
            if password:
                if newpasswd != true_passwd:
                    message = u'2次输入的密码不匹配'
                else:
                    if len(newpasswd) >= 6:
                        try:
                            check_user.set_password(newpasswd)
                            check_user.save()
                            message = u'修改密码成功'
                        except Exception,e:
                            message = e
                    else:
                        message = u"newpasswd小于6位"
            else:
                message =u'旧密码不正确'
    return render_to_response('cmdb/change_passwd.html',{'username':user,'message':message},context_instance=RequestContext(request))
