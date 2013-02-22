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
 y用户信息管理部分
"""

import sys

import hashlib
import setting
import bottle
from bottle import view , route , redirect , request , response , post 
from mode import db,GlobalHtml,ModelTokens
import datetime
from instagram.client import InstagramAPI 
from instagram.oauth2 import OAuth2AuthExchangeError
###获取api 
api = InstagramAPI(client_id=setting.inst_obj.client_id, client_secret=setting.inst_obj.client_secret, redirect_uri=setting.inst_obj.redirect_uri) 



@route("/oauth/inst/login")
def get_inst_login(users=None):
    """
    进入登录设置
    """
    uid     = users.is_login_admin()
    redirect_uri = api.get_authorize_login_url(scope = setting.inst_obj.scope)
    redirect(redirect_uri)


@route("/oauth/inst/access_callback")#,apply=[view("alert")])
def oauth_callback():
    """
    接收token
    """
    ret                 = GlobalHtml().get_ret()
    try:
        token,info      = api.exchange_code_for_access_token(request.query.getu("code"))

        cnf             = {
                        'ptype':'inst',
                        'token':token,
                        'username':info['username'],
                        'puid':str(info['id']),
                        'full_name':info['full_name'],
                        'profile_picture':info['profile_picture']
                }
        
        row           = db.Query(ModelTokens).filter("ptype = ",'inst').get()
        if row is None:
            myTokens        = ModelTokens.get_or_insert(key_name='inst' , **cnf)
            myTokens.put()
        else:
            row.token               = token
            row.profile_picture     = info['profile_picture']
            row.full_name           = info['full_name']
            row.username            = info['username']
            row.puid                = str(info['id'])
            row.put()
        redirect("/pic/inst")
    except OAuth2AuthExchangeError , e:
        ret['message'] = "密钥获取超时"
    return ret



@route("/pic/inst",apply=[view('pic_inst')])
def my_inst_pic_lists(users=None):
    """
    jj界面
    """
    ret                 = GlobalHtml().get_ret()    
    
    query   =   db.Query(ModelTokens)
    row     =   query.filter("ptype = " , 'inst').get()
    
    if row is None:
        ret['message']  =   '没有连接到Instagen <a href="/oauth/inst/login">现在连接</a>' 
        return ret

    api     = InstagramAPI(access_token=row.token)
    recent_media, next = api.user_recent_media()
    #photos  = []
    #for media in recent_media:
    #    photos.append('<img src="%s"/>' % media.images['thumbnail'].url)

    ret['recent_media']    = recent_media
    ret['next']     = next
    return ret





def _post(url):
    """
    post 调用接口
    @ string url 接口完整地址. 
    """
    h               = httplib2.Http()
    return          h.request(url , 'POST')



def _get(url):
    """
    get 调用借口
    """
    h               = httplib2.Http()
    return          h.request(url , 'GET')
