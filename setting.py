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
                'redirect_uri':'http://papa.weilaiu.com/oauth/sina/access_callback',
                'client_secret':'', 
                }




