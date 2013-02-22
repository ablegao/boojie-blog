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


################# 外部类库 ###################################################
import bottle
from bottle import view , route , redirect , request , response, HTTPError
import json
import setting
import datetime
import time
from mode import ModelBlogs , ModelCategory , ModelTags ,db,GlobalHtml


def_content = GlobalHtml()
######应用展示界面相关##############################################
@route("/" ,apply=[view("index")])
@route("/cate/<cate>.html" ,apply=[view("index")])
@route("/tags/<tags>.html" ,apply=[view("index")])
@route("/sitemap.xml" , apply=[view("sitemap")])
def blog_index(cate=None,tags=None,users=None):
    """
    主页
    """
    ret                 = def_content.get_ret()
    ret['login']        = True
    ret['page_title']   = '最近更新'
    user                = users.get_user()
    if user is None or user is False:
        ret['login']    = False 
    
    query               = db.Query(ModelBlogs)
    query.filter('is_del =' , False)
    if cate != None:
        query.filter('cate = ',cate.decode("utf8"))
        ret['page_title']   = cate
    if tags != None:
        query.filter("tags = " , tags.decode("utf8"))

    query.order('-edit_time')
    #for item in query:
    #    print(item.title)
    ret['blog_list']    = query
    return ret


@route("/category" , apply=[view("blog_cate")])
def blog_cate(users=None, glob=None):
    """
    分类列表
    """
    ret                 = def_content.get_ret()
    query               = db.Query(ModelCategory)
    query.filter("is_del = ", False)
    ret['rows']         = query
    return ret

@route("/blog/add" ,method=['POST','GET'] , apply=[view("blog_add")])
def blog_add(users=None , glob = None):
    """
    blog t添加处理时的逻辑
    """
    user    = users.is_login_admin()
    if user is None :
        return 'you need login to me!'
    
    
    ret     = def_content.get_ret()
    title   = request.forms.getu("title",None)
    
    cate    = request.forms.getu("cate",None)
    tags    = request.forms.getu("tags",None)
    content = request.forms.getu("content",None)
    page_id = int(request.query.getu("bid",0))
      
    ret['title']    = title
    ret['cate']     = cate
    ret['tags']     = tags
    ret['content']  = content
    ret['form_url'] = "/blog/add"  
    if page_id >0 :
        row         = ModelBlogs.get_by_id(page_id)
        if row :
            ret['title']    = row.title
            ret['cate']     = row.cate
            ret['tags']     = " ".join(row.tags)
            ret['content']  = row.content
            ret['form_url'] = "/blog/add?bid=%s" % ( page_id, ) 
    ##### cate 处理
    if cate is not None and cate.strip() != '': 
        kwds    =   {'title':cate,'is_del':False}
        cate_mode = ModelCategory.get_or_insert( key_name=cate, **kwds)
        cate_mode.put()

    if tags is not None and tags.strip() != '':
        tag     = tags.split(" ")
        tag     = filter(lambda x:x != "" , tag)
        for x in tag:
            kwds={'title':x,'is_del':False}
            mtag    = ModelTags.get_or_insert(key_name=x,**kwds)
            mtag.put()
    if title and content:
        create_time = datetime.datetime.now()
        if 'tag' not in locals():
            tag     = []
        if page_id >0 :
            row.title   = title
            row.cate    = cate
            row.tags    = tag
            row.content = content
            row.edit_time   = create_time
            row.put()

            redirect("/blog/add?bid=%s" % (page_id,))
        else:
            mblog       = ModelBlogs(account=user , title=title , cate=cate,tags=tag,content=content,create_time=create_time,edit_time=create_time,is_del = False)
            mblog.put()
        #return mblog.key()
    return ret


@route("/l/<bid:int>", apply=[view("blog_info")])
@route("/<catename>/<datey:int>/<datem:int>/<dated:int>/<blog_title>.html", apply=[view("blog_info")])
def blog_info(catename=None,blog_title=None,datey=None , datem=None,dated=None,users=None, glob= None,bid=None):
    """
    x详细信息
    """

    ret                 = def_content.get_ret()
    ret['login']    = users.is_login_admin(redir=False)
    
    if bid != None:
        row         = ModelBlogs.get_by_id(int(bid))
    else:
        query       = db.Query(ModelBlogs)
        query.filter("cate =", catename.decode("utf8")).filter("title =",blog_title.decode('utf8') )
        #query.filter("title =",blog_title.decode("utf8"))
        row         = query.get()


    if row:
        import markdown
        row.html_content = markdown.markdown(row.content)
        ret['row']  = row 
    else:
        raise HTTPError(404,'The page not exists!')
    return ret

@route("/relogin")
def blog_quit(users=None):
    users.set_login()





@route("/get_tags")
def blog_get_tags():
    query           = db.Query(ModelTags)
    ret             = {}
    tags            = []
    for tag in query:
        tags.append(tag.title)
    import json
    return json.dumps(tags)
    #ret['tags'] =