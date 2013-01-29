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

__author__      = "able gao"
__version__     = "0.1"
__license__     = ""

"""
mail 交互部分， 提供进程接口。 
"""
from bottle import Bottle,HTTPError
from bottle import request, response , template




"""
 限定联系api
"""
__link_keys__ = {
        'ablegaoconnectserver':True
        }

def check_link(callback):
    def wrapper(*args,**kwargs):
        if 'authkey' in kwargs and kwargs['authkey']!=None:
            if kwargs['authkey'] in __link_keys__:
                return callback(*args,**kwargs)
                
        raise HTTPError(500,"the link key is error!",500)

        
    return wrapper





app = Bottle()


import setting

app.install(setting.mysql_plugin)




def get_task(db=None ):
    """
    产生用来提供邮件发送的任务列表。 
    """

    ret         = {'users':{}}
    sql         =   "SELECT id,username,mail FROM users WHERE is_del = 0 "
    db.execute(sql)
    userlist    = db.fetchall()
    
    user_conf   = {}
    for user in userlist:
        ret['users'][user['id']]   =   {
                    'name':user['username'],
                    'mail':user['mail'],
                    'uid':user['id'],
                    'tokens':{} 
                }

    # token l列表
    sql         = "SELECT uid,platform_code,platform_id,platform_name,token FROM users_platform_token"
    db.execute(sql)
    tokenlist   = db.fetchall()
    token_count = {}
    for token in tokenlist:
        #token_count["%s_%s_%s" % (token[0],token[1] , token[2])] = token[3]

        if token['platform_code']  not in ret['users'][token['uid']]['tokens']:
            ret['users'][token['uid']]['tokens'][token['platform_code']]           = {}
        ret['users'][token['uid']]['tokens'][token['platform_code']][token['platform_id']]     = {'token':token['token'],'name':token['platform_name'], 'friends':[]}



    sql         = "SELECT uid,platform_code,platform_id,friend_id,platform_last_reply_id FROM users_mail_friends"
    db.execute(sql)
    friends   = db.fetchall()
    for friend in friends:
        ret['users'][friend['uid']]['tokens'][friend['platform_code']][friend['platform_id']]['friends'].append( ( friend['friend_id'] ,int(friend['platform_last_reply_id'])))
        """
        friend_conf             = user_conf[friend[0]]
        k                       = "%s_%s_%s" % (friend[0],friend[1] , friend[2])
        friend_conf['pcode']    = friend[1] #token_count[k]
        friend_conf['pid']      = friend[2]
        friend_conf['uid']      = friend[3]
        friend_conf['last_id']  = friend[4]
        friend_conf['token']    = token_count[k]
        ret['users'].append(friend_conf)
        """
    ret['all_follow_user_count']    = len(friends)
    ret['user_count']               = len(userlist)
    
    return ret

def update_friend_replay_id(db,conf):
    sqls = []
    for uid,pcodetype in conf.items():
        for pcode, puiddict in pcodetype.items():
            for puid , friends in puiddict.items():
                for friend_id , replay_id in friends.items():
                    sql = " UPDATE users_mail_friends SET platform_last_reply_id='%s' WHERE uid=%s AND platform_code='%s' AND platform_id=%s AND friend_id=%s "  % (replay_id , uid,pcode, puid ,friend_id)  
                    db.execute(sql)
    return True


app.route("/mail/get_task",method=["GET",'POST'])
def get_task_from_url(db=None):
    """
    r任务领取， 外部调度接口
    """
    if request.forms.get("key") not in __link_keys__:
        raise HTTPError(500,"the link key is error!",500)
    return get_task(db)

import model.api
import smtplib  
import email.MIMEMultipart# import MIMEMultipart  
import email.MIMEText# import MIMEText  
import email.MIMEBase# import MIMEBase  
import datetime
@app.route("/mail/run<taskname>", method=['GET'])
def mail_run_task_sae(taskname, db=None):
    """
    mail 内部调用url . from sae
    """
    conf = get_task(db)
    if 'users' not in conf or conf['user_count']<=0:
        return "task is emtpy!"

    mail_content    = ''
    '''
    {"all_follow_user_count": 14, "user_count": 1, "users": {"1": {"tokens": {"sina": {"1746727161": {"token": "2.00jWFNuBC15cCEc72fd861a80DoBSn", "friends": [[1722058350, 0], [1759067377, 0], [1898652363, 0], [1750056780, 0], [1774513751, 0], [1954407155, 0], [1353719970, 0], [1974068691, 0], [1228820983, 0], [1839976311, 0], [1732625303, 0], [1865628743, 0], [2147483647, 0], [1742530694, 0]], "name": "\u8d2b\u50e7\u68a6\u6e38"}}}, "mail": "ablegao@gmail.com", "name": "ablegao", "uid": 1}}}
    '''
    title ='趴趴云订阅 %s 期' %  ( datetime.datetime.now().strftime("%Y%m%d%H"), )
    recallData = {}
    for uid,user in conf['users'].items():
        mail        = user['mail']
        username    = user['name']
        data_conf   = {'statuses':[], 'username':username}

        if uid not in recallData:
            recallData[uid] ={}
        for pcode , pidlist in user['tokens'].items():
            #获得对应查询功能api
            if pcode not in recallData[uid]:
                recallData[uid][pcode]={}
            for puid , token_conf in pidlist.items():
                token   = token_conf['token']
                myApi   = model.api.get_api('sina',is_class=True)(token)
                if puid not in recallData[uid][pcode]:
                    recallData[uid][pcode][puid]={}
                for fnumber in xrange(0,len( token_conf['friends'] ) ):
                    friend_id , friend_last_replayid    = token_conf['friends'][fnumber]
                    log     =   myApi.get_user_timeline(uid=friend_id , min =friend_last_replayid  )
                    if friend_id not in recallData[uid][pcode][puid]:
                        recallData[uid][pcode][puid][friend_id] = friend_last_replayid
                    print(log)
                    if log != None and 'statuses' in log:
                        for loginfo in log['statuses']:
                            data_conf['statuses'].append(loginfo)
                            logid   = int(loginfo.get('blogid',0))
                            if logid>  recallData[uid][pcode][puid][friend_id] :
                                recallData[uid][pcode][puid][friend_id]  = logid
        
        if len(data_conf['statuses']) > 0:
            mail_content    = template("mail_template" , data_conf)
            server={
                'host':'smtpout.asia.secureserver.net',
                'user':'papayun@weilaiu.com',
                'passwd':'gaoenbo521',
                }
         
            send_mail(server , "papayun@weilaiu.com" ,mail , title , mail_content)
    
    update_friend_replay_id(db,recallData)
    return " user count %s " % ( str(conf['user_count']) , ) 
#server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject, text, files=[]): 
    main_msg = email.MIMEMultipart.MIMEMultipart()  
    # 构造MIMEText对象做为邮件显示内容并附加到根容器  
    text_msg = email.MIMEText.MIMEText(text,'html',_charset="utf-8")  
    main_msg.attach(text_msg)
    # 设置根容器属性  
    main_msg['From'] = fro  
    main_msg['To'] = to  
    main_msg['Subject'] = subject 
    main_msg['Date'] = email.Utils.formatdate()
    fullText = main_msg.as_string( )  


    import smtplib 
    smtp = smtplib.SMTP(server['host']) 
    smtp.login(server['user'], server['passwd'])
    #smtp.ehlo()
    #smtp.starttls()
    smtp.sendmail(fro, to,fullText) 
    smtp.close()
