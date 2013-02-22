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
 a安全cookie_secret
"""
cookie_secret = "lijseilfnnx,jnv,xjdhfuuhej"

"""
w未登陆时的跳转地址
"""
NOT_LOGIN_REDIRECT = "/login"

"""

数据库配置文件
"""
try:
    import configparser
except ImportError as e:
    import ConfigParser as configparser


"""
 新浪微博授权
"""
oauth2_sina = {
                'oauth_url':'https://api.weibo.com/oauth2',
                'api_url'   :'https://api.weibo.com/2',
                'client_id':'',
                'redirect_uri':'http://www.ablegao.me/oauth/sina/access_callback',
                'client_secret':'', 
                }

"""
 instagram 授权
"""
oauth2_inst = {
                'oauth_url':'https://api.weibo.com/oauth2',
                'api_url'   :'https://api.weibo.com/2',
                'client_id':'53a4c0c978984647a018880eb312b5fd',
                'redirect_uri':'http://www.ablegao.me/oauth/inst/access_callback',
                'client_secret':'18e28464f26540a78ac2d011f0c3755a',
                'scope' :['basic']
                }



class inst_obj(object):
    oauth_url           = oauth2_inst['oauth_url']
    api_url             = oauth2_inst['api_url']
    client_id           = oauth2_inst['client_id']
    redirect_uri        = oauth2_inst['redirect_uri']
    client_secret       = oauth2_inst['client_secret']
    scope               = oauth2_inst['scope']
