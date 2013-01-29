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

from bottle import redirect  , request ,response
import setting
import inspect
from mode import users
"""
y用户登陆， 用户权限相关的一些设置。 
"""


"""

['CreateLoginURL', 'CreateLogoutURL', 'Error', 'GetCurrentUser', 'IsCurrentUserAdmin', 'NotAllowedError', 'RedirectTooLongError', 'User', 'UserNotFoundError', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'apiproxy_errors', 'apiproxy_stub_map', 'create_login_url', 'create_logout_url', 'get_current_user', 'is_current_user_admin', 'os', 'user_service_pb']



"""


class UserLogin(object):
    def __init__(self ):
        pass
    def is_login(self, redir = True):
        """
        s是否登陆 , 登陆状态， 返回登陆id 
        """
        if users.get_current_user() is not None:
            return users.get_current_user()
        else:
            if redir == True :
                redirect(users.create_login_url())
            else:
                return False
    def is_login_admin(self, redir = True):
        """
        s是否登陆 , 登陆状态， 返回登陆id 
        """
        if users.is_current_user_admin():
            return users.get_current_user()
        else:
            if redir == True :
                redirect(users.create_login_url())
            else:
                return False
    
    def is_admin(self):
        return users.IsCurrentUserAdmin

    def set_login(self):
        redirect(users.create_login_url())

    def set_quit(self):
        redirect(users.create_logout_url()) 
    
    def get_user(self):
        return users.get_current_user()

class BottleUsersPlugin(object):
    name = 'users'
    def __init__(self,keyword='users'):
        """
            初始化. keyword 作为def 使用时， 需要传入的量。 
        """
        self.keyword    = keyword
    def setup(self,app):
        """
             插件安装处理
        """
        for other in app.plugins:
            if not isinstance(other, BottleUsersPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another BottleUser plugin with conflicting settings (non-unique keyword).")

    def apply(self,callback, context ):
        args = inspect.getargspec(context['callback'])[0]
        ## 检测用户是否传参 keyword  没有直接执行callback
        if self.keyword not in args:
            return callback
        ## y用户存在需求参数时。
        def wrapper(*args, **kwargs):
            ##给 kwargs。 keyword 负值 .
            kwargs[self.keyword]    = UserLogin( ) 
            rv = callback(*args, **kwargs)
            return rv
        return wrapper

Plugin  =  BottleUsersPlugin


