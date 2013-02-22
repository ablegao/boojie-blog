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



from google.appengine.ext import db
from google.appengine.api import users

class ModelBlogs(db.Model):
    title           = db.StringProperty(required=True)
    cate            = db.StringProperty(required=True)
    tags            = db.StringListProperty()
    content         = db.TextProperty()
    account         = db.UserProperty()
    #new_hire_training_completed = db.BooleanProperty()
    create_time     =   db.DateTimeProperty()
    edit_time       =   db.DateTimeProperty()

    is_del          = db.BooleanProperty(default=False)

class ModelBlogsReply(db.Model):
    blogid          = db.IntegerProperty(required=True)
    account         = db.UserProperty()
    replayid        = db.IntegerProperty()
    content         = db.TextProperty()
    #new_hire_training_completed = db.BooleanProperty()
    create_time     =   db.DateTimeProperty()
    edit_time       =   db.DateTimeProperty()

    is_del          = db.BooleanProperty(default=False)


class ModelCategory(db.Model):
    title           = db.StringProperty(required=True)
    is_del          = db.BooleanProperty(default=False)


class ModelTags(db.Model):
    title           = db.StringProperty(required=True)
    is_del          = db.BooleanProperty(default=False)



class ModelTokens(db.Model):
    ptype            = db.StringProperty(required=True)
    token           = db.StringProperty(required=True)
    username       = db.StringProperty()
    puid            = db.StringProperty()
    full_name       = db.StringProperty()
    profile_picture = db.StringProperty()

class GlobalHtml(object):
    def get_ret(self):
        ret     =   {}
        query   =db.Query( ModelCategory )
        query.filter("is_del = " , False)
        
        ret['menu'] = []
        for cate in query:
            ret['menu'].append( (cate.title,cate.title) )
        return ret
