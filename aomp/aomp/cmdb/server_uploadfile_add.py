#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2014-03-27 22:37:00'
__licence__	= 'GPL licence'

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import forms
import xlrd
from aomp.cmdb.models import Server_all
from add_many_server import add_many_server
class UploadFile(forms.Form):
    filename = forms.FileField()

#保存文件
def handle_uploaded_file(f,file_name):
    with open('cmdb/tempfile/%s' %file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload(request):
    error_remind = []
    error_message = []
    if request.method == "POST":
        uf = UploadFile(request.POST,request.FILES)
        if uf.is_valid():
            file_name = uf.cleaned_data["filename"].name
            if not file_name.endswith(".xls") and not file_name.endswith(".xlsx"):
                print u"不是Excel文件"
            else:
                handle_uploaded_file(request.FILES["filename"],file_name)
                #对excel文件进行处理
                try:
                    file_dir = xlrd.open_workbook(r'cmdb/tempfile/%s' %file_name)
                    handle_table = file_dir.sheets()[0]
                    file_rows = handle_table.nrows
                    for i in xrange(file_rows):
                        content_rows = handle_table.row_values(i)
                        if len(content_rows) == 12:
                            if content_rows[11]:
                                temp_content =  xlrd.xldate_as_tuple(content_rows[11], 0)
                                if len(str(temp_content[1])) < 2:
                                    month = "0" + str(temp_content[1])
                                else:
                                    month = str(temp_content[1])
                                if len(str(temp_content[2])) < 2:
                                    day = "0" + str(temp_content[2])
                                else:
                                    day = str(temp_content[2])
                                year = str(temp_content[0])
                                start_date = year +"-"+ month +"-"+day
                                content_rows[11] = start_date
                            error = add_many_server(content_rows)
                            if error:
                                error_remind.append(("第"+str(i+1)+"行",error))
                        else:
                            error_remind.append(("第"+str(i+1)+"行","请检查字段"))
                    if not error_remind:
                        return HttpResponseRedirect("/cmdb")
                except Exception,e:
                    print e
    else:
        uf = UploadFile()
    return render_to_response('cmdb/server_uploadfile_add.html',{'uf':uf,'mess':error_remind},context_instance=RequestContext(request))
