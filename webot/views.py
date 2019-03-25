from django.shortcuts import render,HttpResponse
from django.http import request
from jira import JIRA


import urllib3
import json
import os
import datetime
import json,threading


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 定义老jira相关信息
options = {
    'server': 'https://xxx.xxx.xxx.xxx:port/jira/',
    'verify': False,
}
jira = JIRA(options, basic_auth=('admin', 'admin'))

# 定义老jira相关信息
options2 = {
    'server': 'http://xxx.xxx.xxx.xxx:8080',
    'verify': False,
}

jira2 = JIRA(options2, basic_auth=('admin', 'admin'))


def index(request):
    if request.method == 'POST':
        print("**********************************************")
        # data = json.dumps(json.loads(request.body),ensure_ascii=False)
        data = json.loads(request.body)
        keynames = data['issue']['fields']['project']['key']
        isstype = data['issue']['fields']['issuetype']['name']
        print(data)
        print("项目代号为"+keynames)
        print("**********************************************")
        # 判断属于SQL工作票类型进行处理
        if keynames == 'SQL':
            if "changelog" not in data:
                print("没有changelog")
            status2 = data['issue']['fields']['status']['name']
            creater = data['issue']['fields']['creator']['displayName']
            issue = data['issue']['key']
            num2 = str(issue.encode('utf-8')).split('-')[1]
            num = num2.strip("'")

            if "comment" not in data:
                appro_info = '无'
            else:
                appro_info = data['comment']['body']
            subject = data['issue']['fields']['summary']
            dangquser = data['user']['displayName']
            url = u"https://xxx.xxx.xxx.xxx:29943/jira/browse/%s"  %issue

            if status2 == u'DBA审核中':
                os.system("python /root/bot/webot/Script/dba.py %s的SQL数据变更申请需要您审批:%s 主题:%s 链接:%s 上一审批人:%s 审批意见:%s 审批格式:%s*同意*同意执行!" %(creater,issue,subject,url,dangquser,appro_info,num))
            if status2 == u'运维负责人审核中':
                os.system("python /root/bot/webot/Script/dba_shenpiwancheng.py [咖啡]%s审批完成,辛苦了[咖啡]" % issue)
                os.system("python /root/bot/webot/Script/leader.py %s的SQL数据变更申请需要您审批:%s 主题:%s 链接:%s 上一审批人:%s 审批意见:%s 审批格式:%s*同意*同意执行!"%(creater,issue,subject,url,dangquser,appro_info,num))
            if status2 == u'正在执行':
                os.system("python /root/bot/webot/Script/ywzx.py %s的SQL数据变更申请需要执行:%s 主题:%s 链接:%s 上一审批人:%s 审批意见:%s"%(creater,issue,subject,url,dangquser,appro_info))
            if status2 == u'执行完毕，等待验证':
                os.system("python /root/bot/webot/Script/deploy_yw.py [咖啡]%s执行完成,辛苦了[咖啡]" % issue)
                os.system("python /root/bot/webot/Script/deploy.py %s的SQL数据变更申请%s已执行完毕，请您及时验证并关闭单子！--主题:%s[咖啡][咖啡][咖啡]"%(creater,issue,subject))
        if keynames == 'XYFZX' and isstype == '客服问题':
            issue = data['issue']['key']
            subject = data['issue']['fields']['summary']
            os.system("python /root/bot/webot/Script/yfzx.py 客服问题SQL申请%s状态已变更：主题：%s"%(issue,subject))
        if keynames == 'NSQL':
            issue = data['issue']['key']
            subject = data['issue']['fields']['summary']

            os.system("python /root/bot/webot/Script/yfzx_sql.py 研发SQL申请%s状态已变更：主题：%s"%(issue,subject))
    return render(request,"index.html")
# Create your views here.
