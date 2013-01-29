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

from mode import db,ModelCategory 
import inspect
class GlobalHtml(object):
    def get_ret(self):
        ret     =   {}
        query   =db.Query( ModelCategory )
        query.filter("is_del = " , False)
        
        ret['menu'] = []
        for cate in query:
            ret['menu'].append( (cate.title,cate.title) )
        
        return ret


class BottleMenuPlugin(object):
    name = 'users'
    def __init__(self,keyword='glob'):
        """
            初始化. keyword 作为def 使用时， 需要传入的量。 
        """
        self.keyword    = keyword
    def setup(self,app):
        """
             插件安装处理
        """
        for other in app.plugins:
            if not isinstance(other, BottleMenuPlugin):
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
            kwargs[self.keyword]    = GlobalHtml( ) 
            rv = callback(*args, **kwargs)
            return rv
        return wrapper

