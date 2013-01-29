#coding:utf-8
#!/usr/bin/env python
#
# Copyright 2013 Able Gao 
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
交互api 部分
"""


from bottle import route,Bottle , redirect , request,install
import setting
from model.api import * 
import json


################# 通用api 部分. ajax 调用######################################################
"""
建立一个提供js 调用的url 组， 

交互用的access_token 从cookie 中获取， 数据由 setting.cookie_secret 加密过 .

/服务/uid。 获取用户id

/<name>/my_follower             我关注的列表
/<name>/follower_me             关注我的列表
/<name>/follower_bilateral      相互关注的列表

"""


@route("/api/<name>/my_follower")
def  api_get_my_friends(name,db=None,users=None):
    """
    获得我的好友
    """
    uid             = users.is_login()
    api_name        = get_api(name)
    
    #if None is not get_api(name):
    if None is api_name:
        return '{"error":"The %s_api is not exists!"}' % (name , ) 
    
    (puid,token)           = users.get_token(name)
    ##获得api 
    api  = globals()[api_name](token)
    
    params          = {}
    params['count'] = request.query.get('count' , 30)
    params['uid']   = puid
    params['trim_status']   =1
    if request.query.get('page' , None):
        params['page'] = request.query.get('page' , None)
    return json.dumps(api.get_my_follower(**params))

@route("/api/<name>/follower_bilateral")
def api_get_follower_bilateral(name,db=None,users=None):
    """
     获取双向关注的数据
    """
    uid             = users.is_login()
    api_name        = get_api(name)
    #if None is not get_api(name):
    if None is api_name:
        return '{"error":"The %s_api is not exists!"}' % (name , ) 
    
    (puid,token)           = users.get_token(name)
    ##获得api 
    api  = globals()[api_name](token)
    params          = {}
    params['count'] = request.query.get('count' , 30)
    if request.query.get('page' , None):
        params['page'] = request.query.get('page' , None)    
    
    return json.dumps(api.get_follower_bilateral(**params))

@route("/api/<name>/follower_me")
def api_get_follower_me(name,db=None,users=None):
    '''
     获取关注我的用户数据
    '''
    uid             = users.is_login()
    api_name        = get_api(name)
    #if None is not get_api(name):
    if None is api_name:
        return '{"error":"The %s_api is not exists!"}' % (name , ) 
    
    (puid,oken)           = users.get_token(name)
    ##获得api

    api  = globals()[api_name](token)
    params          = {}
    params['count'] = request.query.get('count' , 30)
    params['uid']   = uid
    if request.query.get('page' , None):
        params['page'] = request.query.get('page' , None)
    
    return api.get_follower_me(**params )

@route("/api/<name>/uid")
def api_get_uid(name,users=None,db=None):
    """
    获得我的用户id
    """
    api_name        = get_api(name)
    #if None is not get_api(name):
    if None is api_name:
        return '{"error":"The %s_api is not exists!"}' % (name , ) 
    
    puid,token           = users.get_token(name)
    ##获得api 
    api  = globals()[api_name](token)
    
    return json.dumps(api.get_uid())

@route("/api/<name>/atme")
def api_get_atme(name,users=None,db=None):
    api_name        = get_api(name)
    if None is api_name:
        return 
    puid,oken           = users.get_token(name)
    api = globals()[api_name](token)
    return api.get_atme()
