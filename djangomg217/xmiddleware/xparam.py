#coding:utf-8
__author__ = "ila"
import json,copy
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class Xparam(MiddlewareMixin):
    def process_request(self,request):
        fullPath=request.get_full_path()
        print("fullPath===============>",fullPath)
        if "/js/" not in fullPath and "/css/" not in fullPath and "/img/" not in fullPath and "/fonts/" not in fullPath and "/front/" not in fullPath:
            req_dict={}

            #获取query的参数
            for k,v in request.GET.items():
                req_dict[k]=v

            if request.method=="POST":
                contentType=request.META.get('CONTENT_TYPE',"")
                # print("contentType==================>",contentType)
                if "json" in contentType:
                    #解析application/json的参数,如果解析失败,提前返回报错20200925
                    try:
                        data_=json.loads(request.body)
                    except Exception as e:
                        errStr="json loads params error :{} {}".format(Exception,e)
                        print(errStr)
                        msg={"code":500,"msg":errStr}
                        return JsonResponse(msg)
                    if type(data_)==type([1]):
                        req_dict['ids']=data_
                    else:
                        for k,v in data_.items():
                            req_dict[k] = v
                else:
                    # 获取formdata的参数
                    for k, v in request.POST.items():
                        req_dict[k] = v
            #处理参数，去掉无用的和错误的参数
            if req_dict.get("created")!=None:
                req_dict['addtime']=copy.deepcopy(req_dict.get("created"))
                del req_dict["created"]
            if req_dict.get("t") != None:
                del req_dict["t"]
            if req_dict.get("1")!=None:
                req_dict['type']=copy.deepcopy(req_dict.get("1"))
                del req_dict["1"]
            if req_dict.get(1)!=None:
                req_dict['type']=copy.deepcopy(req_dict.get(1))
                del req_dict[1]
            print("req_dict=============+>",req_dict)
            request.session["req_dict"] =req_dict