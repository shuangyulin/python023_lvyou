# coding:utf-8
__author__ = "ila"

from django.db import models

from .model import BaseModel


class users(BaseModel):
    # id=models.BigIntegerField(verbose_name="自增id")
    username = models.CharField(max_length=100, verbose_name=u'账号')
    password = models.CharField(max_length=100, verbose_name=u'密码')
    role = models.CharField(max_length=100, verbose_name=u'角色')
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    __tablename__ = 'users'

    class Meta:
        db_table = 'users'
        verbose_name = verbose_name_plural = u'管理员表'

    # def __str__(self):
    #     return self.username
