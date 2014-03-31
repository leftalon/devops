#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2014-01-23 14:22:49'
__licence__	= 'GPL licence'

#import modules
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from aomp.cmdb.models import Server_all
from django.template import RequestContext
import datetime
import calendar
from aomp.cmdb.server_template_dict import server_template_price
from aomp.cmdb.models import Server_template

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.user_add') == True,login_url='/home')
def month_product_price_total(request):
    message = ''
    now = datetime.datetime.now()
    month_default = now.strftime("%Y-%m")
    #server_all = Server_all.objects.all()
    #服务器去重,得到所有的服务器
    server_all = Server_all.objects.values("server_in_ip","server_out_ip","server_product","server_template_id","server_start_date","server_end_date").distinct()
    month_price_total = 0
    if request.method == "GET":
        month = request.GET.get("month",None)
        if month =='' or month == None:
            month = month_default
        if month == month_default:
            month_one_day = now.strftime("%Y-%m-01")
            month = month_default
            t_year = month.split("-")[0]
            t_month = month.split("-")[1]
            t_day = now.strftime("%d") 
            for server in server_all:
                create_time = server["server_start_date"]
                end_time = server["server_end_date"]
                template_message = Server_template.objects.get(id = server["server_template_id"])
                if template_message:
                    template_price = template_message.template_money
		    if template_price == '':
			template_price = 0
                else:
                    template_price = 0
                if end_time == '' or end_time == None:
                    if create_time < month_one_day:
                        total_day = int(t_day)
                    else:
                        total_day = 1 + int(t_day) - int(create_time.split("-")[2])
                else:
                    if create_time < month_one_day:
                        total_day = int(end_time.split("-")[2])
                    else:
                        total_day = 1 + int(end_time.split("-")[2]) - int(create_time.split("-")[2])
                month_price_total += total_day * float(template_price)
            print "end"
        elif month < month_default:
            t_year = month.split("-")[0]
            t_month = month.split("-")[1]
            month_one_day = "%s-%s-01" %(t_year,t_month)
            t_day = calendar.monthrange(int(t_year),int(t_month))[1]
            month_last_day = "%s-%s-%s" %(t_year,t_month,t_day)
            for server in server_all:
                create_time = server["server_start_date"]
                end_time = server["server_end_date"]
                product = server["server_product"]
                template_message = Server_template.objects.get(id=server["server_template_id"])
                if template_message:
                    template_price = template_message.template_money
		    if template_price == '':
			template_price = 0
                else:
                    template_price = 0
                if end_time == '' or end_time == None:
                    end_time = month_last_day
                    if month_last_day < create_time:
                        total_day = 0
                    elif month_one_day < create_time:
                        total_day = 1 + int(t_day) - int(create_time.split("-")[2])
                    elif month_one_day >= create_time:
                        total_day = int(t_day)
                    else:
                        total_day = 0
                else:
                    if create_time > month_last_day or end_time < month_one_day:
                        total_day = 0
                    elif month_one_day <= create_time and month_last_day >= end_time:
                        total_day = 1 + int(end_time.split("-")[2]) - int(create_time.split("-")[2])
                    elif month_one_day <= create_time and month_last_day <= end_time:
                        total_day = int(t_day)
                    elif month_one_day >= create_time and  month_last_day >= end_time:
                        total_day = int(t_day)
                    elif month_one_day >= create_time and month_last_day <= end_time:
                        total_day = int(end_time.split("-")[2])
                    else:
                        total_day = 0
                month_price_total += total_day * float(template_price)

        else:
            message = u"你所查询的月份比当前月份大"
    return render_to_response("plan_system/month_price_total.html",{'month':month,'message':message,'month_price_total':month_price_total},context_instance=RequestContext(request))
    

@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.user_add') == True,login_url='/home')
def month_plan_system_mingxi(request,date_time):
    server_templateid_name_price = server_template_price()
    #server_all = Server_all.objects.all()
    server_all = Server_all.objects.values("server_in_ip","server_out_ip","server_product","server_template_id","server_start_date","server_end_date").distinct()
    month_price_dict = {}
    product_price_dict = {}
    product_template_price_dict = {}
    #month firest day
    now = datetime.datetime.now()
    now_year_month = now.strftime("%Y-%m")
    month_one_day = "%s-01" %date_time
    #today
    if now_year_month == date_time:
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        month_last_day = now.strftime("%Y-%m-%d")
    else:
        year = date_time.split("-")[0]
        month = date_time.split("-")[1]
        day = calendar.monthrange(int(year),int(month))[1]
        month_last_day = "%s-%s" %(date_time,day)
    for server in server_all:
        create_time = server["server_start_date"]
        end_time = server["server_end_date"]
        product = server["server_product"]
        if end_time == '' or end_time == None:
            end_time = month_last_day
            if month_last_day < create_time:
                total_day = 0
            elif month_one_day < create_time:
                total_day = 1 + int(day) - int(create_time.split("-")[2])
            elif month_one_day >= create_time:
                total_day = int(day)
            else:
                total_day = 0
        else:
            if create_time > month_last_day or end_time < month_one_day:
                total_day = 0
            elif month_one_day <= create_time and month_last_day >= end_time:
                total_day = 1 + int(end_time.split("-")[2]) - int(create_time.split("-")[2])
            elif month_one_day <= create_time and month_last_day <= end_time:
                total_day = int(day)
            elif month_one_day >= create_time and  month_last_day >= end_time:
                total_day = int(day)
            elif month_one_day >= create_time and month_last_day <= end_time:
                total_day = int(end_time.split("-")[2])
            else:
                total_day = 0
        for template_id,template_name_price in server_templateid_name_price.items():
            if server["server_template_id"] == template_id:
                template_name,template_price = template_name_price[0],template_name_price[1]
	        if template_price == '':
		    template_price = 0
                total_price = round(total_day * float(template_price),2)
                if product in product_price_dict:
                    product_price_dict[product] += [[template_name,total_price]]
                else:
                    product_price_dict[product] = [[template_name,total_price]]
    #每个项目中，各个模板的月费用
    for p,tid_price_list in product_price_dict.items():
        temp_dict = {}
        product_total_price = 0.0
        for tid in tid_price_list:
            product_total_price = round(tid[1] + product_total_price,2)
            if tid[0] in temp_dict:
                temp_dict[tid[0]] += tid[1]
            else:
                temp_dict[tid[0]] = tid[1]
        if p not in product_template_price_dict:
            product_template_price_dict[p] = [[temp_dict,product_total_price]]
    return render_to_response("plan_system/month_plan_system_mingxi.html",{'server_templateid_name_price':server_templateid_name_price,'month':date_time,'all_data_dict':product_template_price_dict},context_instance=RequestContext(request))



@login_required
@user_passes_test(lambda u:u.has_perm('hlcmdb.user_add') == True,login_url='/home')
#每天各个项目的的服务器数目
def day_server_num(request,product,month,t_id):
    data = []
    t_id = long(t_id)
    server_templateid_name_price = server_template_price()
    now = datetime.datetime.now()
    day_date = now.strftime("%Y-%m-%d")
    product_server_num_dict = {}
    t_year = month.split("-")[0]
    t_month = month.split("-")[1]
    t_day = calendar.monthrange(int(t_year),int(t_month))[1]
    #月份的天数列表
    day_list = [x+1 for x in range(t_day)]
    for day in day_list:
        if day < 10:
            day = "0" + str(day)
        day_server = []
        template_id = {}
        server_num = 0
        day_str = month + "-" + str(day)
        if day_str > day_date:
            continue
        else:
            server_all = Server_all.objects.values("server_in_ip","server_out_ip","server_product","server_template_id","server_start_date","server_end_date").distinct()
        for one_server in server_all:
            if one_server["server_product"] == product and one_server["server_template_id"] == t_id:
                if one_server["server_end_date"] == None and one_server["server_start_date"] <= day_str:
                    if one_server["server_template_id"] in server_templateid_name_price:
                        template_name = server_templateid_name_price[one_server["server_template_id"]][0]
                    if template_name not in template_id:
                        template_id[template_name] = 1
                    else:
                        template_id[template_name] = template_id[template_name] + 1
                elif one_server["server_end_date"] >= day_str and one_server["server_start_date"] <= day_str:
                    if one_server["server_template_id"] in server_templateid_name_price:
                        template_name = server_templateid_name_price[one_server["server_template_id"]][0]
                    if template_name not in template_id:
                        template_id[template_name] = 1
                    else:
                        template_id[template_name] = template_id[template_name] + 1
                elif one_server["server_end_date"] == '' and one_server["server_start_date"] <= day_str:
                    if one_server["server_template_id"] in server_templateid_name_price:
                        template_name = server_templateid_name_price[one_server["server_template_id"]][0]
                    if template_name not in template_id:
                        template_id[template_name] = 1
                    else:
                        template_id[template_name] = template_id[template_name] + 1
        day_server.append((day_str,template_id))
        if product in product_server_num_dict:
            product_server_num_dict[product] += day_server
        else:
            product_server_num_dict[product] = day_server
    for v in product_server_num_dict.values():
        for mass in v:
            for t,num in mass[1].items():
                data.append([str(mass[0]),num])
    return render_to_response("plan_system/day_server_num.html",{'product_server_num_dict':product_server_num_dict,'data':data},context_instance=RequestContext(request))





