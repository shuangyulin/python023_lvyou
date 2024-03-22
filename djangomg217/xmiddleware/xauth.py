#coding:utf-8
__author__ = "ila"

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.apps import apps

from util.auth import Auth
from util.codes import *
from dj2.settings import dbName as schemaName


class Xauth(MiddlewareMixin):
    def process_request(self,request):
        fullPath = request.get_full_path()
        print("fullPath===============>", fullPath)

        # token=request.META.get("HTTP_TOKEN")
        # print("token=============>",token)
        # request.session['token']=token


        if request.method == 'GET':

            filterList=[
                "/index",
                "/favicon.ico",
                "/login",
                "/register",
                '.js',
                ".css",
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".mp4",
                'mp3',
                ".ttf",
                ".wotf",
                ".woff",
                ".woff2",
                ".otf",
                ".eot",
                ".svg",
                ".csv",
                ".xls",
                ".xlsx",
                ".doc",
                ".docx",
                ".ppt",
                ".pptx",
                ".html",
                ".htm",
                "detail",
                "/forum/flist",
                "/forum/list",
                "/admin",
                "/xadmin",
                "/file/download",
                 "/{}/remind/".format(schemaName),
                  "/{}/option/".format(schemaName),
                "resetPass",
            ]

            allModels = apps.get_app_config('main').get_models()
            for m in allModels:
                try:
                    foreEndList=m.__foreEndList__
                except:
                    foreEndList=None
                if  foreEndList is not None and foreEndList != "前要登":
                    filterList.append("/{}/sendemail".format(m.__tablename__))
                    filterList.append("/{}/list".format(m.__tablename__))

            auth = True

            if fullPath=='/':
                pass
            else:
                for i in filterList:
                    if i in fullPath:
                        auth=False
                if auth==True:
                    result = Auth.identify(Auth, request)

                    if result.get('code') != normal_code:
                        pass
                        #print('jwt auth success')
                        #return JsonResponse(result)
        elif request.method == 'POST':
            post_list = [
                '/{}/defaultuser/register'.format(schemaName),
                '/{}/defaultuser/login'.format(schemaName),
                '/{}/users/register'.format(schemaName),
                '/{}/users/login'.format(schemaName),
                "/{}/examusers/login".format(schemaName),
                "/{}/examusers/register".format(schemaName),
            ]  # 免认证list
            if fullPath not in post_list and "register" not in fullPath and "login" not in fullPath:  # 注册时不检测token。
                result = Auth.identify(Auth, request)

                if result.get('code') != normal_code:
                    print('jwt auth fail')
                    return JsonResponse(result)
