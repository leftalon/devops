# encoding: utf-8
# Create your models here.
from django.db import models
from aomp.cmdb.permission_table import user_permission_list
permissions = user_permission_list

class Server_all(models.Model):
    server_id = models.CharField('唯一标示',max_length=30,unique=True,blank=False)
    server_in_ip = models.CharField('内网ip地址',max_length=30,blank=True)
    server_out_ip = models.CharField('外网ip地址',max_length=30,blank=True)
    server_type = models.CharField('主机类型',max_length=30,blank=False)
    server_template_id = models.IntegerField('主机模板id',max_length=30)
    server_idc_company = models.CharField('IDC所属公司',max_length=30,blank=False)
    server_idc = models.CharField('服务器机房',max_length=30,blank=False)
    server_company = models.CharField('服务器所属公司',max_length=30,blank=False)
    server_product = models.CharField('服务器产品线',max_length=30,blank=False)
    server_group = models.CharField('服务器属于组',max_length=30,blank=False)
    server_status = models.CharField('状态',max_length=30,blank=False)
    server_start_date = models.CharField('服务器创建时间',max_length=30,blank=False)
    server_end_date = models.CharField('服务器结束时间',max_length=30)
    def __unicode__(self):
        return self.server_id
    
    class Meta:
        db_table = 'cmdb'
        ordering = ['server_in_ip']
        permissions = permissions

class Game_type_name(models.Model):
    game_type_name =  models.CharField('游戏平台',max_length=30)
    def __unicode__(self):
        return self.game_type_name
    class Meta:
        db_table = 'game_type_name'

class Game_name_all(models.Model):
    game_type = models.CharField('游戏平台',max_length=30)
    game_name = models.CharField('游戏名称',max_length=30,unique=True,blank=False)
    game_appid = models.CharField('游戏id',max_length=30)
    oper_models = models.CharField('运维模式',max_length=30)
    game_string_id = models.CharField('游戏对应',max_length=30)
    user_name = models.CharField('运维负责人',max_length=30)
    user_phone = models.CharField('运维负责人电话',max_length=30)
    yunying_name = models.CharField('运营负责人',max_length=30)
    yunying_phone = models.CharField('运营人电话',max_length=30)
    backup_yunying_name = models.CharField('第二运营负责人',max_length=30)
    backup_yunying_phone = models.CharField('第二运营人电话',max_length=30)
    developer_name = models.CharField('项目负责人',max_length=30)
    developer_phone = models.CharField('项目负责人电话',max_length=30)
    backup_developer_name = models.CharField('第二项目负责人',max_length=30)
    backup_developer_phone = models.CharField('第二项目负责人电话',max_length=30)
    game_line = models.CharField('游戏状态',max_length=30)
    def __unicode__(self):
        return self.game_name
    class Meta:
        db_table = 'game_name'

class Server_game_group(models.Model):
    group_name = models.CharField('组名称',max_length=30,unique=True,blank=False)
    def __unicode__(self):
        return self.group_name
    class Meta:
        db_table = 'game_group'

class IDC_name_all(models.Model):
    idc_company = models.CharField('公司名称',max_length=30)
    idc_name = models.CharField('IDC名称',max_length=30)
    idc_scode = models.CharField('IDC名称缩写',max_length=30)
    idc_address = models.CharField('IDC地点',max_length=30)
    idc_contact = models.CharField('IDC联系人',max_length=30)
    idc_phone = models.CharField('IDC联系人电话',max_length=30)
    def __unicode__(self):
        return self.idc_name
    class Meta:
        db_table = 'idc_name'

class Server_type_all(models.Model):
    server_type_name = models.CharField('主机类型名称',max_length=30,unique=True,blank=False)
    def __unicode__(self):
        return self.server_type_name
    class Meta:
        db_table = 'server_type_name'

class Server_platform(models.Model):
    platform_name =  models.CharField('平台名称',max_length=30,unique=True,blank=False)
    def __unicode__(self):
        return self.platform_name
    class Meta:
        db_table = 'server_platform'

class Yunweizhiban_table(models.Model):
    zhiban_day = models.CharField('值班时间',max_length=30,unique=True,blank=False)
    baiban_name = models.CharField('白班值班人员',max_length=30)
    yeban_name = models.CharField('夜班值班人员',max_length=30)
    def __unicode__(self):
        return self.zhiban_day
    class Meta:
        ordering = ['zhiban_day']
        db_table = 'yunweizhiban_table'

class Server_template(models.Model):
    template_name = models.CharField('主机模板名称',max_length=30,unique=True,blank=False)
    template_model = models.CharField('服务器型号',max_length=30)
    template_cpu = models.CharField('服务器cpu',max_length=30,blank=False)
    template_mem = models.CharField('服务器内存',max_length=30,blank=False)
    template_disk = models.CharField('服务器磁盘',max_length=30,blank=False)
    template_money = models.CharField('服务器价格',max_length=30,default=0)
    def __unicode__(self):
        return self.template_name
    class Meta:
        db_table = 'server_template'

class Event_record(models.Model):
    name = models.CharField('姓名',max_length=30,blank=False)
    event = models.CharField('事件',max_length=500,blank=False)
    time = models.CharField('时间',max_length=30,blank=False)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'event_table'

class Remark_table(models.Model):
    date = models.CharField('日期',max_length=30,blank=False)
    remark = models.CharField('备注',max_length=500)
    author = models.CharField('添加人',max_length=30,blank=False)
    add_date = models.CharField('添加日期',max_length=30,blank=False)
    status = models.CharField('状态',max_length=30,blank=False)
    dealer_name = models.CharField('操作人',max_length=30)
    def __unicode__(self):
        return self.date
    class Meta:
        ordering = ['-add_date']
        db_table = 'remark_table'
