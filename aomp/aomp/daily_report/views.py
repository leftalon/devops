#encoding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from aomp.daily_report.models import Year_Month_table,Mapping_table,Days_table
import time,datetime

# Create your views here.
@login_required
def daily_report(request):
    temp_days_all = []
    days_in_this_month = {}
    this_year = time.strftime("%Y", time.localtime(time.time()))
    this_month = time.strftime("%m", time.localtime(time.time()))                   
    this_day = time.strftime("%d", time.localtime(time.time()))
    month_day = str(int(this_month)) + u'月' + str(int(this_day)) + u'日'
    year_month = this_year + u'年' + str(int(this_month)) + u'月'
    if request.method == 'POST':
        reports = request.POST.get('comments', None)
        user = str(request.user)
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if Email_table.objects.filter(spell=user):
            name = Email_table.objects.get(spell=user).username
            sql = Days_table(days=month_day,months=year_month,name=name,spell=request.user,time=now_time,content=reports)
            try:
                sql.save()
                return HttpResponseRedirect('/daily_report')
            except Exception,e:
                message = e
    months_all = Year_Month_table.objects.all()
    reports_all = Days_table.objects.filter(days=month_day,months=year_month)
    days_all = Mapping_table.objects.all()
    return render_to_response("daily_report/daily_report_today.html",{'months_all':months_all,'days_all':days_all,'reports_all':reports_all},context_instance=RequestContext(request))

@login_required
def daily_report_day(request,id):
    day_id = 0
    year_month = ''
    month_day = ''
    other_day = ''
    if id:
        day_id = int(id)
    months_all = Year_Month_table.objects.all()
    days_all = Mapping_table.objects.all()
    this_year = time.strftime("%Y", time.localtime(time.time()))
    this_month = time.strftime("%m", time.localtime(time.time()))
    this_day = time.strftime("%d", time.localtime(time.time()))
    if Mapping_table.objects.filter(id=day_id):
        month_day = Mapping_table.objects.get(id=day_id).days
        year_month = Mapping_table.objects.get(id=day_id).year_month
        other_day = month_day
        if request.method == 'POST':
            reports = request.POST.get('comments', None)
            user = str(request.user)
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            if Email_table.objects.filter(spell=user):
                name = Email_table.objects.get(spell=user).username
                sql = Days_table(days=month_day,months=year_month,name=name,spell=user,time=now_time,content=reports)
                try:
                    sql.save()
                except Exception,e:
                    message = e
    if not month_day:
        month_day = str(int(this_month)) + u'月' + str(int(this_day)) + u'日'
    reports_all = Days_table.objects.filter(days=month_day,months=year_month)
    if not other_day:
        return render_to_response("daily_report/daily_report_today.html",{'months_all':months_all,'days_all':days_all,'reports_all':reports_all},context_instance=RequestContext(request))
    return render_to_response("daily_report/daily_report_other_day.html",{'months_all':months_all,'days_all':days_all,'reports_all':reports_all,'other_day':other_day},context_instance=RequestContext(request))

@login_required
def daily_report_edit(request,id):
    day_id = 0
    report = ''
    message = ''
    this_year = time.strftime("%Y", time.localtime(time.time()))
    this_month = time.strftime("%m", time.localtime(time.time()))
    this_day = time.strftime("%d", time.localtime(time.time()))
    month_day = str(int(this_month)) + u'月' + str(int(this_day)) + u'日'
    months_all = Year_Month_table.objects.all()
    days_all = Mapping_table.objects.all()

    if id:
        day_id = int(id)
    if not Days_table.objects.filter(id=day_id):
        message = '未知错误'
    else:
        report = Days_table.objects.get(id=day_id)
        if request.method == 'POST':
            content = request.POST.get('comments',None)
            if content and str(request.user) == report.spell:
                Days_table.objects.filter(id=day_id).update(content=content)
                return HttpResponseRedirect('/daily_report')
            else:
                message = '未知错误'

    return render_to_response("daily_report/daily_report_edit.html",{'message':message,'months_all':months_all,'days_all':days_all,'report':report},context_instance=RequestContext(request))
