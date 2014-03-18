#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2013-12-18 14:31:47'
__licence__	= 'GPL licence'

#import modules
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext
from hlcmdb.models import Server_template
from hlcmdb.pagination import pagination_django
from django.http import HttpResponseRedirect
from hlcmdb.models import Event_record
import datetime

@login_required
def template_show(request):
    if request.method == 'GET':
        template_all = Server_template.objects.all()
        template_count = template_all.count()
        page_num = request.GET.get('page',1)
        if page_num != 'all':
            page_num = int(page_num)
        page_list,page_up,page_next,frist_page,last_page,page_all_data,last_page_value = pagination_django(template_all,15,page_num)
    return render_to_response('cmdb/template_show.html',{'template_all':page_all_data,'template_count':template_count,'page_num':page_num,'last_page_value':last_page_value,'game_all_name':page_all_data,'page_list':page_list,'page_up':page_up,'page_next':page_next,'frist_page':frist_page,'last_page':last_page},context_instance=RequestContext(request))

@login_required
def template_add(request):
    template_name = ''
    template_model = ''
    template_cpu = ''
    template_mem = ''
    template_disk = ''
    template_money = ''
    message = ''
    if request.method == 'POST':
        template_name = request.POST.get('template_name',None)
        template_model = request.POST.get('template_model',None)
        template_cpu = request.POST.get('template_cpu',None)
        template_mem = request.POST.get('template_mem',None)
        template_disk = request.POST.get('template_disk',None)
        template_money = request.POST.get('template_money',0)
        if template_name == '' or template_name == None:
            message = u'模板名称不能为空'
        else:
            if Server_template.objects.filter(template_name=template_name):
                message = u'模板名称已经存在'
            else:
                template_add = Server_template(template_name=template_name,template_model=template_model,template_cpu=template_cpu,template_mem=template_mem,template_disk=template_disk,template_money=template_money)
                if template_add:
                    try:
                        template_add.save()
                        message = u'%s模板添加成功' %template_name
                        event = u'模板添加成功，模板名称为:%s' %template_name
                        print event
                        sql = Event_record(name=request.user,event=event,time=datetime.datetime.now())
                        sql.save()
                    except Exception,e:
                        message = e
                else:
                    message = u'插入数据error'
    return render_to_response('cmdb/template_add.html',{'template_name':template_name,'template_model':template_model,'template_cpu':template_cpu,'template_mem':template_mem,'template_disk':template_disk,'template_money':template_money,'message':message},context_instance = RequestContext(request))

@login_required
def template_edit(request,temp_id):
    message = ''
    temp_id = int(temp_id)
    one_template = Server_template.objects.get(id=temp_id)
    if request.method == 'POST':
        template_name = request.POST.get('template_name',None)
        template_model = request.POST.get('template_model',None)
        template_cpu = request.POST.get('template_cpu',None)
        template_mem = request.POST.get('template_mem',None)
        template_disk = request.POST.get('template_disk',None)
        template_money = request.POST.get('template_money',None)
        update_template = Server_template.objects.filter(id=temp_id).update(template_name=template_name,template_model=template_model,template_cpu=template_cpu,template_mem=template_mem,template_disk=template_disk,template_money=template_money)
        if update_template:
            new_template = Server_template.objects.get(id=temp_id)
            event=u'模板编辑成功，更改前内容%s,更改后内容为%s' %(one_template,new_template)
            sql=Event_record(name=request.user,event=event,time=datetime.datetime.now())
            sql.save()
            return HttpResponseRedirect('/cmdb/template_show')
    return render_to_response('cmdb/template_edit.html',{'message':message,'one_template':one_template},context_instance = RequestContext(request))
