#encoding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^home/$','aomp.cmdb.views.home'),
    url(r'^$', lambda x: HttpResponseRedirect('/login/')),
    url(r'^cmdb/$','aomp.cmdb.views.query_server'),
    url(r'^cmdb/in_ip=(\d+\.\d+\.\d+\.\d+)&out_ip=(\d+\.\d+\.\d+\.\d+)/$','aomp.cmdb.views.query_server_search'),
    url(r'^cmdb/in_ip=(\d+\.\d+\.\d+\.\d+:\d+)&out_ip=(\d+\.\d+\.\d+\.\d+)/$','aomp.cmdb.views.query_server_search'),
    url(r'^cmdb/(\w+?)=(\w+?)$','aomp.cmdb.views.field_show'),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'cmdb/login.html'}, name='login'),
    url(r'^logout/$', 'aomp.cmdb.views.logout_view'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cmdb/home/$', 'aomp.cmdb.views.home', name='home'),
    #负责人联系方式
    url(r'^cmdb/admin_game/$','aomp.cmdb.admin_game.admin_game'),
    #运维值班表
    url(r'^cmdb/yunweizhiban/$','aomp.cmdb.yunweizhiban.yunweizhiban'),
    url(r'^cmdb/yunweizhiban_add/$','aomp.cmdb.yunweizhiban.yunweizhiban_add'),
    url(r'^cmdb/yunweizhiban_edit&id=(\d+?)/$','aomp.cmdb.yunweizhiban.yunweizhiban_edit'),
    url(r'^cmdb/yunweizhiban_edit_mode/$','aomp.cmdb.yunweizhiban.yunweizhiban_edit_mode'),
    url(r'^cmdb/server_group/$','aomp.cmdb.views.server_group'),
    url(r'^cmdb/server_group_add/$','aomp.cmdb.views.server_group_add'),
    #服务器模板展示
    url(r'^cmdb/template_show/$','aomp.cmdb.server_template.template_show'),
    url(r'^cmdb/template_add/$','aomp.cmdb.server_template.template_add'),
    url(r'^cmdb/template_edit&id=(\d+?)/$','aomp.cmdb.server_template.template_edit'),
    #服务器添加
    url(r'^cmdb/server_add/$','aomp.cmdb.views.server_add'),
    url(r'^cmdb/server_many_add/$','aomp.cmdb.views.server_many_add'),
    url(r'^cmdb/server_uploadfile_add/$','aomp.cmdb.server_uploadfile_add.upload'),
    url(r'^cmdb/server_simplify_add/$','aomp.cmdb.views.server_simplify_add'),
    #服务器删除
    url(r'^cmdb/server_del/$','aomp.cmdb.views.server_del'),
    #服务器编辑
    url(r'^cmdb/server_edit&id=(\d{1,4})&server_product=(\w+?)/$','aomp.cmdb.views.server_edit'),
    url(r'^cmdb/one_server_del&id=(\d{1,4})&server_product=(\w+?)/$','aomp.cmdb.views.one_server_del'),
    #IDC管理
    url(r'^cmdb/idc_all/$','aomp.cmdb.views.idc_all'),
    url(r'^cmdb/idc_add/$','aomp.cmdb.views.idc_add'),
    url(r'^cmdb/idc_edit&id=(\d{1,4})/$','aomp.cmdb.views.idc_edit'),
    #游戏管理
    url(r'^cmdb/game_all/$','aomp.cmdb.views.game_all'),
    url(r'^cmdb/game_add/$','aomp.cmdb.views.game_add'),
    url(r'^cmdb/game_edit&id=(\d{1,4})/$','aomp.cmdb.views.game_edit'),
    #组用户管理
    url(r'^cmdb/user_all/$','aomp.cmdb.views.user_all'),
    url(r'^cmdb/user_add/$','aomp.cmdb.views.user_add'),
    url(r'^cmdb/permission_builder/$','aomp.cmdb.permission_builder.permission_table'),
    #修改自己密码
    url(r'^cmdb/change_passwd/$','aomp.cmdb.change_passwd.change_passwd'),
    #为其他用户修改密码
    url(r'^cmdb/reset_password/$','aomp.cmdb.views.reset_password_for_other_user'),
    #备注添加/编辑/删除
    url(r'^cmdb/remark&remark_date=(\d{8})/$','aomp.cmdb.yunweizhiban.remark_show'),
    url(r'^cmdb/remark_add&remark_date=(\d{8})/$','aomp.cmdb.yunweizhiban.remark_add'),
    url(r'cmdb/remark_edit&id=(\d+)/$','aomp.cmdb.yunweizhiban.remark_edit'),
    url(r'cmdb/remark_delete&id=(\d+)/$','aomp.cmdb.yunweizhiban.remark_delete'),
    #
    url(r'^salt_auto/command$','aomp.salt_auto.views.command'),
    url(r'^salt_auto/minion$','aomp.salt_auto.views.minion'),
    #
    url(r'^puppet/$','aomp.puppet_config.views.puppet'),
    url(r'^puppet/nid=(\d+?)$','aomp.puppet_config.views.node_pp_config'),
    url(r'^puppet/host_config_add$','aomp.puppet_config.views.host_config_add'),
    url(r'^puppet/delete_node_id=(\d+?)$','aomp.puppet_config.views.delete_node_id'),
    url(r'^puppet/update_node_id=(\d+?)$','aomp.puppet_config.views.update_node_id'),
    #日报系统
    url(r'^daily_report/$','aomp.daily_report.views.daily_report'),
    url(r'^daily_report/pageid=(\d+)$','aomp.daily_report.views.daily_report_day'),
    url(r'^daily_report/edit/msgid=(\d+)$','aomp.daily_report.views.daily_report_edit'),
    )
