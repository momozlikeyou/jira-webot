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
            zhuangtai = ' '
        else:
            zhuangtai = data['changelog']['items'][0]['toString']
        #zhuangtai = data['changelog']['items'][0]['toString']
        zhuangtai2 = data['issue']['fields']['status']['name']
        #q_zhuangtai = data['changelog']['items'][0]['fromString']
        creater = data['issue']['fields']['creator']['displayName']
        issue = data['issue']['key']
        bianhao2 = str(issue.encode('utf-8')).split('-')[1]
        bianhao = bianhao2.strip("'")
        print("状态为:"+zhuangtai)
        print("状态为："+zhuangtai2)
        print("创建者为:"+creater)
        print("issue为:"+issue)
        print("编号为"+bianhao)
        if ( "comment" not in data ):
            appro_info = '无'
            op = '无'
        else:
            appro_info = data['comment']['body']
            op = data['comment']['author']['displayName']
        jibie = data['issue']['fields']['priority']['name']
        zhuti = data['issue']['fields']['summary']
        miaoshu = data['issue']['fields']['description']
        dangquser = data['user']['displayName']
        daishenpiren = data['issue']['fields']['customfield_10800']['displayName']
        url = u"https://211.160.73.226:29943/jira/browse/%s"  %issue
        print("审批意见为："+appro_info)
        print("级别为："+jibie)
        print("主题为："+zhuti)
        print("dangquser为："+dangquser)
        print("待审批人为："+daishenpiren)
        print("执行人为："+op)
        if zhuangtai2 == u'DBA审核中':
            os.system("python /root/bot/webot/dba.py %s的SQL数据变更申请需要您审批:%s 主题:%s 链接:%s 上一审批人:%s 审批意见:%s 审批格式:%s*同意*同意执行!" %(creater,issue,zhuti,url,dangquser,appro_info,bianhao))
        if zhuangtai2 == u'运维负责人审核中':
            os.system("python /root/bot/webot/dba_shenpiwancheng.py [咖啡]%s审批完成,辛苦了[咖啡]"%(issue))
            os.system("python /root/bot/webot/leader.py %s的SQL数据变更申请需要您审批:%s 主题:%s 链接:%s 上一审批人:%s 审批意见:%s 审批格式:%s*同意*同意执行!"%(creater,issue,zhuti,url,dangquser,appro_info,bianhao))
        if zhuangtai2 == u'正在执行':
            os.system("python /root/bot/webot/ywzx.py %s的SQL数据变更申请需要执行:%s 主题:%s 链接:%s 上一审批人:%s 审批意见:%s"%(creater,issue,zhuti,url,dangquser,appro_info))
        if zhuangtai2 == u'执行完毕，等待验证':
            os.system("python /root/bot/webot/deploy_yw.py [咖啡]%s执行完成,辛苦了[咖啡]"%(issue))
            os.system("python /root/bot/webot/deploy.py %s的SQL数据变更申请%s已执行完毕，请您及时验证并关闭单子！--主题:%s[咖啡][咖啡][咖啡]"%(creater,issue,zhuti))
    return render(request,"index.html")


#*******************定时任务判断统计运维负责人审核、DBA审核、正在执行阶段********************************\
def check_wang_jira():
    issue1 = jira.search_issues('project = "SQL" and  status = "运维负责人审核中" and updated >= -1d')
    j = []
    for i in issue1:
        j.append('{0}'.format(i))
    long1 = len(j)
    strlong1 = str(long1)
    joinj =",".join(j)

    if long1 == 0:
        os.system("python /root/bot/webot/leader_wan.py 24小时内提交的数据变更已全部审批完成")
    else:
        os.system("python /root/bot/webot/leader_wei_wan.py 24小时内提交的数据变更,还有%s条需要审批%s"%(strlong1,joinj))

    t = threading.Timer(7200, check_wang_jira)
    t.start()
t = threading.Timer(7200,check_wang_jira)
t.start()



def check_dba_jira():
    issue3 = jira.search_issues('project = "SQL" and  status = "DBA审核中" and updated >= -1d')
    l = []
    for g in  issue3:
        l.append('{0}'.format(g))
    long3 = len(l)
    strlong3 = str(long3)
    joinl =",".join(l)
    if long3 == 0:
        os.system("python /root/bot/webot/dba_wan.py 24小时内提交的数据变更已全部审批完成")
    else:
        os.system("python /root/bot/webot/dba_wei_wan.py 24小时内提交的数据变更，还有%s条需要审批%s"%(strlong3,joinl))

    t = threading.Timer(7200, check_dba_jira)
    t.start()
t = threading.Timer(7200,check_dba_jira)
t.start()

def check_op_jira():
    issue2 = jira.search_issues('project = "SQL" and  status = "正在执行" and updated >= -1d')
    k = []
    for h in  issue2:
        k.append('{0}'.format(h))
    long2 = len(k)
    strlong2 = str(long2)
    joink = ",".join(k)
    
    if long2 == 0:
        os.system("python /root/bot/webot/ywzx_wan.py 24小时内提交的数据变更已全部执行完成")
    else:
        os.system("python /root/bot/webot/ywzx_wei_wan.py 24小时内提交的数据变更，还有%s条需要执行%s"%(strlong2,joink))

    t = threading.Timer(7200, check_op_jira)
    t.start()
t = threading.Timer(7200,check_op_jira)
t.start()
# Create your views here.
