#encoding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^home/$','cmdb.hlcmdb.views.home'),
    url(r'^$', lambda x: HttpResponseRedirect('/login/')),
    url(r'^cmdb/$','cmdb.hlcmdb.views.query_server'),
    url(r'^cmdb/in_ip=(\d+\.\d+\.\d+\.\d+)&out_ip=(\d+\.\d+\.\d+\.\d+)/$','cmdb.hlcmdb.views.query_server_search'),
    url(r'^cmdb/in_ip=(\d+\.\d+\.\d+\.\d+:\d+)&out_ip=(\d+\.\d+\.\d+\.\d+)/$','cmdb.hlcmdb.views.query_server_search'),
    url(r'^cmdb/(\w+?)=(\w+?)$','cmdb.hlcmdb.views.field_show'),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'cmdb/login.html'}, name='login'),
    url(r'^logout/$', 'cmdb.hlcmdb.views.logout_view'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cmdb/home/$', 'cmdb.hlcmdb.views.home', name='home'),
    #负责人联系方式
    url(r'^cmdb/admin_game/$','cmdb.hlcmdb.admin_game.admin_game'),
    #运维值班表
    url(r'^cmdb/yunweizhiban/$','cmdb.hlcmdb.yunweizhiban.yunweizhiban'),
    url(r'^cmdb/yunweizhiban_add/$','cmdb.hlcmdb.yunweizhiban.yunweizhiban_add'),
    url(r'^cmdb/yunweizhiban_edit&id=(\d+?)/$','cmdb.hlcmdb.yunweizhiban.yunweizhiban_edit'),
    #服务器模板展示
    url(r'^cmdb/template_show/$','cmdb.hlcmdb.server_template.template_show'),
    url(r'^cmdb/template_add/$','cmdb.hlcmdb.server_template.template_add'),
    url(r'^cmdb/template_edit&id=(\d+?)/$','cmdb.hlcmdb.server_template.template_edit'),
    #服务器添加
    url(r'^cmdb/server_add/$','cmdb.hlcmdb.views.server_add'),
    url(r'^cmdb/server_many_add/$','cmdb.hlcmdb.views.server_many_add'),
    #服务器删除
    url(r'^cmdb/server_del/$','cmdb.hlcmdb.views.server_del'),
    #服务器编辑
    url(r'^cmdb/server_edit&id=(\d{1,4})&server_product=(\w+?)/$','cmdb.hlcmdb.views.server_edit'),
    url(r'^cmdb/one_server_del&id=(\d{1,4})&server_product=(\w+?)/$','cmdb.hlcmdb.views.one_server_del'),
    #IDC管理
    url(r'^cmdb/idc_all/$','cmdb.hlcmdb.views.idc_all'),
    url(r'^cmdb/idc_add/$','cmdb.hlcmdb.views.idc_add'),
    url(r'^cmdb/idc_edit&id=(\d{1,4})/$','cmdb.hlcmdb.views.idc_edit'),
    #服务器类型管理
    url(r'^cmdb/game_all/$','cmdb.hlcmdb.views.game_all'),
    url(r'^cmdb/game_add/$','cmdb.hlcmdb.views.game_add'),
    url(r'^cmdb/game_edit&id=(\d{1,4})/$','cmdb.hlcmdb.views.game_edit'),
    #组用户管理
    url(r'^cmdb/user_all/$','cmdb.hlcmdb.views.user_all'),
    url(r'^cmdb/user_add/$','cmdb.hlcmdb.views.user_add'),
    url(r'^cmdb/permission_builder/$','cmdb.hlcmdb.permission_builder.permission_table'),
    #修改自己密码
    url(r'^cmdb/change_passwd/$','cmdb.hlcmdb.change_passwd.change_passwd'),
    #为其他用户修改密码
    url(r'^cmdb/reset_password/$','cmdb.hlcmdb.views.reset_password_for_other_user'),
)
