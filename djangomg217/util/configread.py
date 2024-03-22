#coding:utf-8
__author__ = "ila"
from configparser import ConfigParser

def config_read(filePath:str):
    cfg=ConfigParser()
    cfg.read(filePath)
    if "sql" in cfg.sections():
        dbType=cfg.get('sql','type')
        host=cfg.get('sql','host')
        port=cfg.getint('sql','port')
        user=cfg.get('sql','user')
        passwd=cfg.get('sql','passwd')
        dbName=cfg.get('sql','db')
        charset=cfg.get('sql','charset')
        return dbType,host,port,user,passwd,dbName,charset
    else:
        return None,None,None,None,None,None,None