from django.db import models

# Create your models here.
#class Foo(models.Model):
#    caption = models.CharField(max_length=16)

class UserType(models.Model):
    '''
    用户类型
    '''
    title = models.CharField(max_length=64)
#    fo = models.ForeignKey('Foo')


class UserInfo(models.Model):
    '''
    用户表
    '''
    name = models.CharField(max_length=64)
    age = models.IntegerField()
    ut = models.ForeignKey("UserType")