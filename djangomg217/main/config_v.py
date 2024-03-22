# coding:utf-8
__author__ = "ila"

import logging

from django.http import JsonResponse

from .config_model import config
from util.codes import *
from util import message as mes


def config_page(request):
    '''
    获取参数信息
    :return:
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,
               "data": {"currPage": 1, "totalPage": 1, "total": 1, "pageSize": 10, "list": []}}
        req_dict = request.session.get('req_dict')
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize'] = config.page(config, config, req_dict)
        return JsonResponse(msg)


def config_list(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,
               "data": {"currPage": 1, "totalPage": 1, "total": 1, "pageSize": 10, "list": []}}
        req_dict = request.session.get("req_dict")

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize'] = config.page(config, config, req_dict)

        return JsonResponse(msg)


def config_info(request, id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = config.getbyid(config, config, int(id_))
        if len(data) > 0:
            msg['data'] = data[0]
        return JsonResponse(msg)


def config_detail(request, id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = config.getbyid(config, config, int(id_))
        if len(data) > 0:
            msg['data'] = data[0]
        return JsonResponse(msg)


def config_save(request):
    '''
    创建参数信息
    :return:
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        req_dict = request.session.get('req_dict')
        param1 = config.getbyparams(config, config, req_dict)
        if param1:
            msg['code'] = id_exist_code
            msg['msg'] = mes.id_exist_code
            return JsonResponse(msg)

        error = config.createbyreq(config, config, req_dict)
        logging.warning("save_config.res=========>{}".format(error))
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def config_add(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        error = config.createbyreq(config, config, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def config_update(request):
    '''
    更新参数信息
    :return:
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        req_dict = request.session.get('req_dict')

        config.updatebyparams(config, config, req_dict)

        return JsonResponse(msg)


def config_delete(request):
    '''
    删除参数信息
    :return:
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        req_dict = request.session.get('req_dict')
        config.deletes(config,
            config,
            req_dict.get("ids")
        )

        return JsonResponse(msg)
