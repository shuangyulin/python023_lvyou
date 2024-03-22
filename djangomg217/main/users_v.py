# coding:utf-8
__author__ = "ila"

from django.http import JsonResponse

from .users_model import users
from util.codes import *
from util.auth import Auth
import util.message as mes


def users_login(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")
        if req_dict.get('role')!=None:
            del req_dict['role']
        datas = users.getbyparams(users, users, req_dict)
        if not datas:
            msg['code'] = password_error_code
            msg['msg'] = mes.password_error_code
            return JsonResponse(msg)

        req_dict['id'] = datas[0].get('id')
        return Auth.authenticate(Auth, users, req_dict)


def users_register(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")

        error = users.createbyreq(users, users, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def users_session(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg":mes.normal_code, "data": {}}

        req_dict = {"id": request.session.get('params').get("id")}
        msg['data'] = users.getbyparams(users, users, req_dict)[0]

        return JsonResponse(msg)


def users_logout(request):
    if request.method in ["POST", "GET"]:
        msg = {
            "msg": "退出成功",
            "code": 0
        }

        return JsonResponse(msg)


def users_page(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,
               "data": {"currPage": 1, "totalPage": 1, "total": 1, "pageSize": 10, "list": []}}
        req_dict = request.session.get("req_dict")
        tablename = request.session.get("tablename")
        try:
            __hasMessage__ = users.__hasMessage__
        except:
            __hasMessage__ = None
        if __hasMessage__ and __hasMessage__ != "否":

            if tablename != "users":
                req_dict["userid"] = request.session.get("params").get("id")
        if tablename == "users":
            msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
            msg['data']['pageSize'] = users.page(users, users, req_dict)
        else:
            msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
            msg['data']['pageSize'] = [],1,0,0,10

        return JsonResponse(msg)


def users_info(request, id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = users.getbyid(users, users, int(id_))
        if len(data) > 0:
            msg['data'] = data[0]
        # 浏览点击次数
        try:
            __browseClick__ = users.__browseClick__
        except:
            __browseClick__ = None

        if __browseClick__ and "clicknum" in users.getallcolumn(users, users):
            click_dict = {"id": int(id_), "clicknum": str(int(data[0].get("clicknum", 0)) + 1)}
            ret = users.updatebyparams(users, users, click_dict)
            if ret != None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg)


def users_save(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        error = users.createbyreq(users, users, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def users_update(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if req_dict.get("mima") and req_dict.get("password"):
            if "mima" not in users.getallcolumn(users,users):
                del req_dict["mima"]
            if "password" not in users.getallcolumn(users,users):
                del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass
        error = users.updatebyparams(users, users, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def users_delete(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        error = users.deletes(users,
            users,
            req_dict.get("ids")
        )
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)
