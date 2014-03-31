#encoding:utf-8

from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Year_Month_table(models.Model):
    year_month = models.CharField('年月',max_length=30,unique=True,blank=False)
    def __unicode__(self):
        return self.year_month
    class Meta:
        db_table = 'year_month_table'

class Mapping_table(models.Model):
    year_month = models.CharField('年月',max_length=30,blank=False)
    days = models.CharField('日',max_length=30,unique=True,blank=False)
    def __unicode__(self):
        return self.year_month
    class Meta:
        db_table = 'mapping_table'

class Days_table(models.Model):
    days = models.CharField('日',max_length=30,blank=False)
    months = models.CharField('年月',max_length=30,blank=False)
    name = models.CharField('姓名',max_length=30,blank=False)
    spell = models.CharField('拼写',max_length=30,blank=False)
    time = models.CharField('时间',max_length=30,blank=False)
    content = HTMLField()
    def __unicode__(self):
        return self.days
    class Meta:
        db_table = "days_table"
        ordering = ["-time"]
    
