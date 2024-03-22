# coding:utf-8
__author__ = "ila"

from django.db import models

from .model import BaseModel


class config(BaseModel):
    # id=models.BigIntegerField(verbose_name="自增id")
    name = models.CharField(max_length=100, verbose_name=u'键名')
    value = models.CharField(max_length=100, verbose_name=u'键值')

    __tablename__ = 'config'

    class Meta:
        db_table = 'config'
        verbose_name = verbose_name_plural = u'配置表'

    # def __str__(self):
    #     return self.name
