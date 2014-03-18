from django.db import models

# Create your models here.
class Group_role(models.Model):
    game_name = models.CharField(max_length=200,unique=True,blank=False)
    group_role_name = models.CharField(max_length=200,blank=False)
    def __unicode(self):
        return self.group_role_name

    class Meta:
        db_table = "group_role"

class Member_role(models.Model):
    group_role_name = models.CharField(max_length=200)
    member_role_name = models.CharField(max_length=200)
    member_in_ip = models.CharField(max_length=200,blank=False)
    def __unicode(self):
        return self.group_role_name

    class Meta:
        db_table = "member_role"

