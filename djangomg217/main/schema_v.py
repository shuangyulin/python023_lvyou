# coding:utf-8
__author__ = "ila"

import logging, os, time

from django.http import JsonResponse
from django.apps import apps
from wsgiref.util import FileWrapper
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect

from .config_model import config
from util.codes import *
from util import message as mes
from util.baidubce_api import BaiDuBce
from util.locate import geocoding
from dj2.settings import dbName as schemaName

def schemaName_cal(request, tableName, columnName):
    '''
    计算规则接口
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, 'data': []}
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:

                data = m.getcomputedbycolumn(
                    m,
                    m,
                    columnName
                )
                print(data)
                if data:
                    try:
                        sum='%.05f' % float(data.get("sum"))
                    except:
                        sum=0.00
                    try:
                        max='%.05f' % float(data.get("max"))
                    except:
                        max=0.00
                    try:
                        min='%.05f' % float(data.get("min"))
                    except:
                        min=0.00
                    try:
                        avg='%.05f' % float(data.get("avg"))
                    except:
                        avg=0.00
                    msg['data'] = {
                        "sum": sum,
                        "max": max,
                        "min": min,
                        "avg": avg,
                    }
                break

        return JsonResponse(msg)


def schemaName_file_upload(request):
    '''
    上传
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}

        file = request.FILES.get("file")

        if file:
            filename = file.name
            filesuffix = filename.split(".")[-1]
            file_name = "{}.{}".format(int(float(time.time()) * 1000), filesuffix)
            filePath = os.path.join(os.getcwd(), "templates/front", file_name)
            print("filePath===========>", filePath)

            with open(filePath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            msg["file"] = file_name
            # 判断是否需要保存为人脸识别基础照片
            req_dict = request.session.get("req_dict")
            type1 = req_dict.get("type", 0)
            print("type1=======>",type1)
            type1 = int(type1)
            if type1 == 1:
                params = {"name":"faceFile","value": file_name}
                config.createbyreq(config, config, params)
        return JsonResponse(msg)


def schemaName_file_download(request):
    '''
    下载
    '''
    if request.method in ["POST", "GET"]:
        req_dict = request.session.get("req_dict")
        filename = req_dict.get("fileName")

        filePath = os.path.join(os.getcwd(), "templates/front", filename)
        print("filePath===========>", filePath)

        file = open(filePath, 'rb')
        response = HttpResponse(file)

        response['Content-Type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filePath)
        response['Content-Length'] = os.path.getsize(filePath)
        return response


def schemaName_follow_level(request, tableName, columnName, level, parent):
    '''

    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, 'data': []}
        # 组合查询参数
        params = {
            "level": level,
            "parent": parent
        }

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                data = m.getbyparams(
                    m,
                    m,
                    params
                )
                # 只需要此列的数据
                for i in data:
                    msg['data'].append(i.get(columnName))
                break
        return JsonResponse(msg)


def schemaName_follow(request, tableName, columnName):
    '''
    根据option字段值获取某表的单行记录接口
    组合columnName和columnValue成dict，传入查询方法
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, 'data': []}
        # 组合查询参数
        params = request.session.get('req_dict')
        columnValue = params.get("columnValue")
        params = {columnName: columnValue}

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                data = m.getbyparams(
                    m,
                    m,
                    params
                )
                if len(data)>0:
                    msg['data'] = data[0]
                break

        return JsonResponse(msg)


def schemaName_location(request):
    '''
    定位
    :return:
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "address": ''}
        req_dict = request.session.get('req_dict')

        datas = config.getbyparams(config, config, {"name": "baidu_ditu_ak"})
        if len(datas) > 0:
            baidu_ditu_ak = datas[0].get("baidu_ditu_ak")
        else:
            baidu_ditu_ak = 'QvMZVORsL7sGzPyTf5ZhawntyjiWYCif'
        lat = req_dict.get("lat", 24.2943350100)
        lon = req_dict.get("lng", 116.1287866600)
        msg['address'] = geocoding(baidu_ditu_ak, lat, lon)

        return JsonResponse(msg)


def schemaName_matchface(request):
    '''
    baidubce百度人脸识别
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code}
        req_dict = request.session.get("req_dict")

        face1 = req_dict.get("face1")
        file_path1 = os.path.join(os.getcwd(),"templates/front",face1)

        face2 = req_dict.get("face1")
        file_path2 = os.path.join(os.getcwd(), "templates/front", face2)

        data = config.getbyparams(config, config, {"name": "APIKey"})
        client_id = data[0].get("APIKey")
        data = config.getbyparams(config, config, {"name": "SecretKey"})
        client_secret = data[0].get("SecretKey")

        bdb = BaiDuBce()
        score = bdb.bd_check2pic(client_id, client_secret, file_path1, file_path2)
        msg['score'] = score

        return JsonResponse(msg)


def schemaName_option(request, tableName, columnName):
    '''
    获取某表的某个字段列表接口
    :param request:
    :param tableName:
    :param columnName:
    :return:
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, 'data': []}

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                data = m.getbyColumn(
                    m,
                    m,
                    columnName
                )

                msg['data'] = data
                break
        return JsonResponse(msg)


def schemaName_remind_tablename_columnname_type(request, tableName, columnName, type)->int:
    '''
    前台提醒接口（通用接口，不需要登陆）
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, 'data': []}
        # 组合查询参数
        params = request.session.get("req_dict")
        remindstart = int(params.get('remindstart')) if params.get('remindstart') != None else None
        remindend = int(params.get('remindend')) if params.get('remindend') != None else None
        if int(type) == 1:  # 数字
            if remindstart == None and remindend != None:
                params['remindstart'] = 0
            elif remindstart != None and remindend == None:
                params['remindend'] = 999999
            elif remindstart == None and remindend == None:
                params['remindstart'] = 0
                params['remindend'] = 999999
        elif int(type) == 2:  # 日期
            current_time = int(time.time())
            if remindstart == None and remindend != None:
                starttime = current_time - 60 * 60 * 24 * 365 * 2
                params['remindstart'] = time.strftime("%Y-%m-%d", time.localtime(starttime))
                endtime = current_time + 60 * 60 * 24 * remindend
                params['remindend'] = time.strftime("%Y-%m-%d", time.localtime(endtime))

            elif remindstart != None and remindend == None:
                starttime = current_time - 60 * 60 * 24 * remindstart
                params['remindstart'] = time.strftime("%Y-%m-%d", time.localtime(starttime))
                endtime = current_time + 60 * 60 * 24 * 365 * 2
                params['remindend'] = time.strftime("%Y-%m-%d", time.localtime(endtime))
            elif remindstart == None and remindend == None:
                starttime = current_time - 60 * 60 * 24 * 365 * 2
                params['remindstart'] = time.strftime("%Y-%m-%d", time.localtime(starttime))
                endtime = current_time + 60 * 60 * 24 * 365 * 2
                params['remindend'] = time.strftime("%Y-%m-%d", time.localtime(endtime))

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                data = m.getbetweenparams(
                    m,
                    m,
                    columnName,
                    params
                )

                msg['count'] = len(data)
                break
        return JsonResponse(msg)


def schemaName_tablename_remind_columnname_type(request, tableName, columnName, type):
    '''
    后台提醒接口，判断authSeparate和authTable的权限
    '''
    if request.method in ["POST", "GET"]:
        print("schemaName_tablename_remind_columnname_type==============>")
        msg = {"code": normal_code, 'data': []}

        req_dict = request.session.get("req_dict")
        remindstart = int(req_dict.get('remindstart')) if req_dict.get('remindstart')!=None else None
        remindend = int(req_dict.get('remindend')) if req_dict.get('remindend')!=None else None
        print("req_dict===================>",req_dict)
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                tableModel=m
                break
        # 获取全部列名
        columns = tableModel.getallcolumn(tableModel, tableModel)

        # 当前登录用户所在表
        tablename = request.session.get("tablename")
        # 当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为”是”，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__ =tableModel.__authTables__
        except:
            __authTables__ = {}

        if __authTables__ != {}:

            for authColumn, authTable in __authTables__.items():
                if authTable == tablename:
                    params = request.session.get("params")
                    req_dict[authColumn] = params.get(authColumn)
                    break


        '''__authSeparate__此属性为真，params添加userid，后台只查询个人数据'''
        try:
            __authSeparate__ =tableModel.__authSeparate__
        except:
            __authSeparate__ = None

        if __authSeparate__ == "是":
            tablename = request.session.get("tablename")
            if tablename != "users" and 'userid' in columns:
                try:
                    pass
                    # req_dict['userid'] = request.session.get("params").get("id")
                except:
                    pass

        # 组合查询参数
        if int(type) == 1:  # 数字
            if remindstart == None and remindend != None:
                req_dict['remindstart'] = 0
            elif remindstart != None and remindend == None:
                req_dict['remindend'] = 999999
            elif remindstart == None and remindend == None:
                req_dict['remindstart'] = 0
                req_dict['remindend'] = 999999
        elif int(type) == 2:  # 日期
            current_time = int(time.time())
            if remindstart == None and remindend != None:
                starttime = current_time - 60 * 60 * 24 * 365 * 2
                req_dict['remindstart'] = time.strftime("%Y-%m-%d", time.localtime(starttime))
                endtime = current_time + 60 * 60 * 24 * remindend
                req_dict['remindend'] = time.strftime("%Y-%m-%d", time.localtime(endtime))

            elif remindstart != None and remindend == None:
                starttime = current_time - 60 * 60 * 24 * remindstart
                req_dict['remindstart'] = time.strftime("%Y-%m-%d", time.localtime(starttime))
                endtime = current_time + 60 * 60 * 24 * 365 * 2
                req_dict['remindend'] = time.strftime("%Y-%m-%d", time.localtime(endtime))
            elif remindstart == None and remindend == None:
                starttime = current_time - 60 * 60 * 24 * 365 * 2
                req_dict['remindstart'] = time.strftime("%Y-%m-%d", time.localtime(starttime))
                endtime = current_time + 60 * 60 * 24 * 365 * 2
                req_dict['remindend'] = time.strftime("%Y-%m-%d", time.localtime(endtime))
            else:
                starttime = current_time - 60 * 60 * 24 * remindstart
                req_dict['remindstart'] = time.strftime("%Y-%m-%d", time.localtime(starttime))
                endtime = current_time + 60 * 60 * 24 * remindend
                req_dict['remindend'] = time.strftime("%Y-%m-%d", time.localtime(endtime))
        print("req_dict==============>",req_dict)
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                data = m.getbetweenparams(
                    m,
                    m,
                    columnName,
                    req_dict
                )

                msg['count'] = len(data)
                break
        return JsonResponse(msg)

def schemaName_sh(request, tableName):
    '''
    根据主键id修改table表的sfsh状态接口
    '''
    if request.method in ["POST", "GET"]:
        print('tableName=========>', tableName)
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        req_dict = request.session.get("req_dict")
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:

                # 查询结果
                data1 = m.getbyid(
                    m,
                    m,
                    req_dict.get('id')
                )
                if data1[0].get("sfsh") == '是':
                    req_dict['sfsh'] = '否'
                else:
                    req_dict['sfsh'] = '否'

                # 更新
                res = m.updatebyparams(
                    m,
                    m,
                    req_dict
                )
                # logging.warning("schemaName_sh.res=====>{}".format(res))
                if res!=None:
                    msg["code"]=crud_error_code
                    msg["code"]=mes.crud_error_code
                break
        return JsonResponse(msg)


def schemaName_upload(request, fileName):
    '''
    '''
    if request.method in ["POST", "GET"]:
        return HttpResponseRedirect  ("/{}/front/{}".format(schemaName,fileName))


def schemaName_group_quyu(request, tableName, columnName):
    '''
    {
    "code": 0,
    "data": [
        {
            "total": 2,
            "shangpinleibie": "水果"
        },
        {
            "total": 1,
            "shangpinleibie": "蔬菜"
        }
    ]
    }
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                msg['data'] = m.groupbycolumnname(
                    m,
                    m,
                    columnName
                )
                break

        return JsonResponse(msg)


def schemaName_value_quyu(request, tableName, xColumnName, yColumnName):
    '''
    按值统计接口,
    {
    "code": 0,
    "data": [
        {
            "total": 10.0,
            "shangpinleibie": "aa"
        },
        {
            "total": 20.0,
            "shangpinleibie": "bb"
        },
        {
            "total": 15.0,
            "shangpinleibie": "cc"
        }
    ]
}
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                msg['data'] = m.getvaluebyxycolumnname(
                    m,
                    m,
                    xColumnName,
                    yColumnName
                )
                break

        return JsonResponse(msg)
