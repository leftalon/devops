#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2013-12-04 14:48:19'
__licence__	= 'GPL licence'
#import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from aomp.cmdb.models import Yunweizhiban_table
import datetime
from django.http import HttpResponseRedirect
from aomp.cmdb.weekday import weekday
from django.db.models import Q
from aomp.cmdb.models import Event_record,Remark_table
from aomp.cmdb.operation_models import remark_status

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def yunweizhiban(request):
    week_d = {}
    name_num = {}
    now = datetime.datetime.now()
    string = now.strftime("%Y-%m")
    today = now.strftime("%Y-%m-%d")
    days = []
    yunweizhiban = Yunweizhiban_table.objects.all()
    remarks = Remark_table.objects.all()
    for i in remarks:
        days.append(i.date[0:4] + i.date[5:7] +i.date[8:10])
    days = list(set(days))
    for week in yunweizhiban:
        s = week.zhiban_day
        week_str = week.zhiban_day.split("-")
        week_date = datetime.date(int(week_str[0]),int(week_str[1]),int(week_str[2]))
        week_day = week_date.weekday()
        week_weekday = weekday.get(week_day)
        if s not in week_d:
            week_d[s] = week_weekday
    if request.method == "GET":
        search_date = request.GET.get("search_date",'')
        if search_date == None or search_date == '':
            yunweizhiban = yunweizhiban
        else:
            search_content = search_date
            yunweizhiban = Yunweizhiban_table.objects.filter(Q(zhiban_day__contains=search_content) | Q(baiban_name__contains=search_content) | Q(yeban_name__contains=search_content))
    	for week in yunweizhiban:
            s = week.zhiban_day
            week_str = week.zhiban_day.split("-")
            week_date = datetime.date(int(week_str[0]),int(week_str[1]),int(week_str[2]))
            week_day = week_date.weekday()
            week_weekday = weekday.get(week_day)
            if s not in week_d:
                week_d[s] = week_weekday
	
    return render_to_response("cmdb/yunweizhiban.html",{'search_date':search_date,'week_d':week_d,'today':today,'yunweizhiban':yunweizhiban,'days':days},context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def yunweizhiban_add(request):
    message = []
    zhiban = []
    event = ''
    arrange = 1
    if request.method == "POST":
        many_information = request.POST.get('many_yunweizhiban',None)
        if many_information == '' or many_information == None:
            message.append(u"请输入要添加的值班信息表")
        else:
            for one_information in many_information.strip().split("\n"):
                one_information = one_information.split()
                if len(one_information) != 3:
                    message.append(u"%s请检查信息格式"%one_information)
                else:
                    date = one_information[0]
                    baiban = one_information[1]
                    yeban = one_information[2]
                    if Yunweizhiban_table.objects.filter(zhiban_day=date):
                        message.append(u'%s已经存在'%date)
                    else:
                        ywzb_sql = Yunweizhiban_table(zhiban_day=date,baiban_name=baiban,yeban_name=yeban)
                        if ywzb_sql:
                            try:
                                ywzb_sql.save()
                                if arrange == 1:
                                        zhiban.append(u'添加值班信息成功，日期:%s，白班:%s，夜班:%s' %(date,baiban,yeban))
                                else:
                                        zhiban.append(u'日期:%s，白班:%s，夜班:%s' %(date,baiban,yeban))
                                arrange += 1
                            except Exception,e:
                                message.append(e)
    for element in zhiban:
         event = event + '\t' + element
    if event:
         sql=Event_record(name=request.user,event=event,time=datetime.datetime.now())
         sql.save()
    return render_to_response('cmdb/yunweizhiban_add.html',{'message':message},context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def yunweizhiban_edit(request,setid):
    message = ''
    id = int(setid)
    id_content = Yunweizhiban_table.objects.get(id=id)
    if request.method == "POST":
        zhiban_day = request.POST.get('zhiban_day')
        baiban_name = request.POST.get('baiban_name',None)
        yeban_name = request.POST.get('yeban_name',None)
        if baiban_name == '' or baiban_name == None:
            message = u'白班值班人不能为空'
        elif yeban_name == '' or yeban_name == None:
            message = u'夜班值班人不能为空'
        else:
            update_sql = Yunweizhiban_table.objects.filter(id=id).update(baiban_name=baiban_name,yeban_name=yeban_name)
            if update_sql:
                event=u'编辑值班信息成功，日期:%s，新的安排为：白班是%s，夜班是%s' %(zhiban_day,baiban_name,yeban_name)
                sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                sql.save()
                return HttpResponseRedirect('/cmdb/yunweizhiban')
            else:
                message = u"修改不成功"
    return render_to_response("cmdb/yunweizhiban_edit.html",{'message':message,'yunweizhiban':id_content},context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def yunweizhiban_edit_mode(request):
    week_d = {}
    name_num = {}
    now = datetime.datetime.now()
    string = now.strftime("%Y-%m")
    today = now.strftime("%Y-%m-%d")
    yunweizhiban = Yunweizhiban_table.objects.all()
    for week in yunweizhiban:
        s = week.zhiban_day
        week_str = week.zhiban_day.split("-")
        week_date = datetime.date(int(week_str[0]),int(week_str[1]),int(week_str[2]))
        week_day = week_date.weekday()
        week_weekday = weekday.get(week_day)
        if s not in week_d:
            week_d[s] = week_weekday
    if request.method == "GET":
        search_date = request.GET.get("search_date",'')
        if search_date == None or search_date == '':
            yunweizhiban = yunweizhiban
        else:
            search_content = search_date
            yunweizhiban = Yunweizhiban_table.objects.filter(Q(zhiban_day__contains=search_content) | Q(baiban_name__contains=search_content) | Q(yeban_name__contains=search_content))
        for week in yunweizhiban:
            s = week.zhiban_day
            week_str = week.zhiban_day.split("-")
            week_date = datetime.date(int(week_str[0]),int(week_str[1]),int(week_str[2]))
            week_day = week_date.weekday()
            week_weekday = weekday.get(week_day)
            if s not in week_d:
                week_d[s] = week_weekday
    return render_to_response("cmdb/yunweizhiban_edit_mode.html",{'search_date':search_date,'week_d':week_d,'today':today,'yunweizhiban':yunweizhiban},context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def remark_add(request,remark_date):
    message = ''
    date = remark_date[0:4] + '-' + remark_date[4:6] + '-' + remark_date[6:8]
    today = datetime.datetime.now().strftime("%m-%d %H:%M")
    remark = ''
    if remark:
        sql = Remark_table(date=date,remark=temp,author=request.user,add_date=today,status='未处理')
        sql.save()
    return HttpResponseRedirect('/cmdb/remark&remark_date='+remark_date)

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def remark_edit(request, id):
    message = ''
    remark = ''
    status = ''
    if Remark_table.objects.filter(id=id):
        remark = Remark_table.objects.get(id=id)
        date = remark.date
    if request.method == "POST":
        new_remark = request.POST.get('remark_name')
        status = request.POST.get('status_name')
        dealer_name = request.POST.get('dealer_name')
        Remark_table.objects.filter(id__exact=id).update(remark=new_remark,status=status,dealer_name=dealer_name)
        temp_date = date[0:4] + date[5:7] + date[8:10]
        return HttpResponseRedirect('/cmdb/remark&remark_date='+temp_date)
    date = date[0:4] + date[5:7] + date[8:10]
    return render_to_response("cmdb/remark_edit.html",{'message':message,'remark':remark,'date':date,'remark_status':remark_status},context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def remark_show(request,remark_date):
    date = remark_date[0:4] + '-' + remark_date[4:6] + '-' + remark_date[6:8]
    today = datetime.datetime.now().strftime("%m-%d %H:%M")
    remarks = []
    temp_remarks = []
    if request.method == "POST":
        remark = request.POST.get('remark')
        if remark:
            sql = Remark_table(date=date,remark=remark,author=request.user,add_date=today,status='未处理')
            sql.save()
    if Remark_table.objects.filter(date=date):
        temp_remarks = Remark_table.objects.all()
        for i in temp_remarks:
            if i.date == date:
                remarks.append(i)
    return render_to_response("cmdb/remark.html",{'remarks':remarks,'date':remark_date},context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.see_all_server') == True,login_url='/home')
def remark_delete(request,id):
    id = int(id)
    date = ''
    if Remark_table.objects.filter(id=id):
        date = Remark_table.objects.get(id=id).date
        date = date[0:4] + date[5:7] + date[8:10]
        Remark_table.objects.filter(id__exact=id).delete()
        return HttpResponseRedirect('/cmdb/remark&remark_date='+date)
    else:
        return HttpResponseRedirect('/cmdb/yunweizhiban')
