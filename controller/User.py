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
import hashlib
import setting
import bottle
from bottle import view , route , redirect , request , response , post 
import re
import datetime


@route("/login" , apply=[view('login')] , method=['GET' , 'POST'])
def user_login(db,users):
    """
    用户登陆业务
    """
    db              = db.cursor()
    username        = request.forms.get("username" ,    None)
    passwd          = request.forms.get("passwd",       None)
    ret             = {'menu_id':0 , 'msg':''}
    if username != None and passwd != None:
        md5pass = hashlib.md5(passwd.encode(encoding="gb2312"))
        passwd  = md5pass.hexdigest()

        sql         = "SELECT id , username,mail FROM users WHERE username = %(user)s and passwd = %(passwd)s and is_del = 0"
        db.execute(sql, {
                    'user':username , 
                    'passwd':passwd
            })
        row = db.fetchone()
        if row != None:
            #( id , username , mail ) = row
            id      = row['id']
            username= row['username']
            mail    = row['mail']
            sql     = "UPDATE users SET login_time =%(login_time)s , login_ip = %(login_ip)s  , logincount=logincount+1 WHERE id=%(ids)s"
            db.execute(sql , {
                    'login_ip':request.environ.get('REMOTE_ADDR') , 
                    'login_time':datetime.datetime.now(),
                    'ids': id 
                })
            users.set_login(id)
            ret['msg']  = '登陆成功！'
            redirect("/")
        else:
            ret['msg']  = '用户名/密码可能不正确！'
        return ret
    else:
        return ret


@route("/user_invite"  , apply=[view("users_invite")] )
def user_invite():
    """
    账户邀请业务处理
    """
    
    rex     = r'^([0-9]{10})$'
    success = ''
    code = request.query.get("code" , None)
    if code is None:
        success=''
    elif code == '':
        success= '邀请代码不能为空'

    elif re.match(rex,code) == None:
        success = '格式错误!'
    else:
        response.set_cookie("re_code",'comeform')
        redirect("/userrregist")
    return {'menu_id':0, 'success':success}



@route("/user_regist", apply=[view("user_regist")]  , method=['POST' , 'GET'])
def user_regist(db):
    """
        用户注册功能。 
    """
    db              = db.cursor()
    #if request.get_cookie("re_code" , None) != 'comeform':
    #    redirect("/user_invite")
    #else:
    #    return {"main_id":0}
    username        = request.forms.get("username" ,    None)
    passwd          = request.forms.get("passwd",       None)
    comfirm_passwd  = request.forms.get("comfirm_passwd",None)
    nickname        = request.forms.get("nickname",     None)
    mail            = request.forms.get("mail",         None)
    msg             =''


    ret = {'menu_id':0 , 'msg':''}
    if username is not None :
        if passwd is not None and passwd !=''   \
                and passwd  == comfirm_passwd   \
                and mail is not None and mail !='':

            sql="SELECT * FROM users WHERE (username = %(user)s or mail = %(mail)s ) and is_del=0"
            db.execute(sql , {"user":username , "mail":mail})
            row  = db.fetchone()
            if row != None:
                ret['msg'] = '账户已经存在'
                db.close()
                return ret
            sql="insert into users (username , passwd , nickname , mail , regist_ip, regist_time , is_del) values " \
                "(%(username)s , %(passwd)s , %(nickname)s , %(mail)s , %(regist_ip)s , %(regist_time)s , 0)"
            
            md5pass = hashlib.md5(passwd.encode(encoding="gb2312"))
            passwd  = md5pass.hexdigest()
            db.execute(sql, {
                'username':username,
                'passwd':passwd,
                'nickname':nickname,
                'mail':mail,
                'regist_ip':request.environ.get('REMOTE_ADDR'),
                'regist_time':datetime.datetime.now()
                })
            db.close()
            ret['msg'] = '注册成功!'
            redirect("/login")
        else:
            ret['msg'] = '数据错误!'

    return ret


@route("/quit" )
def user_quit(users=None, db=None):
    users.set_quit()
    users.is_login()
