from django.shortcuts import render,HttpResponse
from django.http import request
from jira import JIRA


import urllib3
import json
import os
import datetime
import json,threading


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

options = {
    'server': 'https://211.160.73.226:29943/jira/',
    'verify': False,
}
jira = JIRA(options, basic_auth=('admin', 'AdminYwzx'))



def index(request):
    if request.method == 'POST':
        print("**********************************************")
        #data = json.dumps(json.loads(request.body),ensure_ascii=False)
        data = json.loads(request.body)
        print(data)
        print("**********************************************")
        if ( "changelog" not in data ):
            print("没有changelog")
            status = ' '
        else:
            status = data['changelog']['items'][0]['toString']
        status2 = data['issue']['fields']['status']['name']
        creater = data['issue']['fields']['creator']['displayName']
        issue = data['issue']['key']
        num2 = str(issue.encode('utf-8')).split('-')[1]
        num = num2.strip("'")

        if ( "comment" not in data ):
            appro_info = '无'
            op = '无'
        else:
            appro_info = data['comment']['body']
            op = data['comment']['author']['displayName']
        property = data['issue']['fields']['priority']['name']
        subject = data['issue']['fields']['summary']
        describ = data['issue']['fields']['description']
        dangquser = data['user']['displayName']
        url = u"https://211.160.73.226:29943/jira/browse/%s"  %issue

        if status2 == u'DBA审核中':
            os.system("python /root/bot/webot/Script/dba.py %s的SQL数据变更申请需要您审批:%s 主题:%s 链接:%s 上一审批人:%s 审批意见:%s 审批格式:%s*同意*同意执行!" %(creater,issue,subject,url,dangquser,appro_info,num))
        if status2 == u'运维负责人审核中':
            os.system("python /root/bot/webot/Script/dba_shenpiwancheng.py [咖啡]%s审批完成,辛苦了[咖啡]"%(issue))
            os.system("python /root/bot/webot/Script/leader.py %s的SQL数据变更申请需要您审批:%s 主题:%s 链接:%s 上一审批人:%s 审批意见:%s 审批格式:%s*同意*同意执行!"%(creater,issue,subject,url,dangquser,appro_info,num))
        if status2 == u'正在执行':
            os.system("python /root/bot/webot/Script/ywzx.py %s的SQL数据变更申请需要执行:%s 主题:%s 链接:%s 上一审批人:%s 审批意见:%s"%(creater,issue,subject,url,dangquser,appro_info))
        if status2 == u'执行完毕，等待验证':
            os.system("python /root/bot/webot/Script/deploy_yw.py [咖啡]%s执行完成,辛苦了[咖啡]"%(issue))
            os.system("python /root/bot/webot/Script/deploy.py %s的SQL数据变更申请%s已执行完毕，请您及时验证并关闭单子！--主题:%s[咖啡][咖啡][咖啡]"%(creater,issue,subject))
    return render(request,"index.html")
# Create your views here.
