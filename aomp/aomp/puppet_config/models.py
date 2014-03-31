#!/usr/bin/env python
#encoding:utf-8
from django.db import models

# Create your models here.

class Node_config_message(models.Model):
    node_name = models.CharField('node名字',max_length=200,unique=True,blank=False)
    cmdb_id = models.CharField('cmdb中得ID',max_length=200,unique=True,blank=False)
    items_name = models.CharField('所属项目',max_length=200,blank=False)
    group_name = models.CharField('所属组名',max_length=200,blank=False)
    private_ip = models.CharField('私有ip',max_length=200)
    public_ip = models.CharField('公有ip',max_length=200)
    include_modules = models.CharField('include模板',max_length=200)
    node_file = models.TextField()
    def __unicode__(self):
        return self.__node_name
    class Meta:
        db_table = 'node_config_message'
        ordering = ["group_name","node_name"]
