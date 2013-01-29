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

import sys,os
sys.path.insert(0,"other.zip")
""" 
bottle 版 url 处理
"""
from bottle import Bottle
import bottle
from bottle import view, route, request , default_app , mount ,run
from bottle import debug
bottle.FormsDict.getu = bottle.FormsDict.getunicode
debug(True)
import setting


bottle.TEMPLATE_PATH = ['./templates/default']



#bottle.install(setting.mysql_plugin)
import plugin.user_login
import plugin.cate_menu

bottle.install(plugin.user_login.Plugin())

#import controller.User
#import controller.api
import controller.blog
#import controller.mail


#mount("/mapi" , controller.mail.app)

if __name__ =='__main__':
    run(host='localhost' , port = "8080" , debug= True , reloader= True)
else:
    application = default_app()

