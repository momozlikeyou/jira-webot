# 定时任务，定时查询运维负责人、DBA审核、正在执行阶段jira数量并进行推送


from jira import JIRA

import urllib3
import os
import json, threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 定义连接系统

options = {
    'server': 'https://xxx:xxx:xxx:xxx:port/jira/',
    'verify': False,
}
jira = JIRA(options, basic_auth=('admin', 'xxx'))


# *******************定时任务判断统计运维负责人审核阶段********************************

def check_wang_jira():
    issue1 = jira.search_issues('project = "SQL" and  status = "运维负责人审核中" and updated >= -1d')
    j = []
    for i in issue1:
        j.append('{0}'.format(i))
    long1 = len(j)
    strlong1 = str(long1)
    joinj = ",".join(j)

    if long1 == 0:
        os.system("python /root/bot/webot/Script/leader_wan.py 24小时内提交的数据变更已全部审批完成")
    else:
        os.system("python /root/bot/webot/Script/leader_wei_wan.py 24小时内提交的数据变更,还有%s条需要审批%s" % (strlong1, joinj))

    t = threading.Timer(7200, check_wang_jira)
    t.start()


t = threading.Timer(7200, check_wang_jira)
t.start()


# *******************定时任务判断统计DBA审核阶段********************************
def check_dba_jira():
    issue3 = jira.search_issues('project = "SQL" and  status = "DBA审核中" and updated >= -1d')
    l = []
    for g in issue3:
        l.append('{0}'.format(g))
    long3 = len(l)
    strlong3 = str(long3)
    joinl = ",".join(l)
    if long3 == 0:
        os.system("python /root/bot/webot/Script/dba_wan.py 24小时内提交的数据变更已全部审批完成")
    else:
        os.system("python /root/bot/webot/Script/dba_wei_wan.py 24小时内提交的数据变更，还有%s条需要审批%s" % (strlong3, joinl))

    t = threading.Timer(7200, check_dba_jira)
    t.start()


t = threading.Timer(7200, check_dba_jira)
t.start()


# *******************定时任务判断统计正在执行阶段********************************
def check_op_jira():
    issue2 = jira.search_issues('project = "SQL" and  status = "正在执行" and updated >= -1d')
    k = []
    for h in issue2:
        k.append('{0}'.format(h))
    long2 = len(k)
    strlong2 = str(long2)
    joink = ",".join(k)

    if long2 == 0:
        os.system("python /root/bot/webot/Script/ywzx_wan.py 24小时内提交的数据变更已全部执行完成")
    else:
        os.system("python /root/bot/webot/Script/ywzx_wei_wan.py 24小时内提交的数据变更，还有%s条需要执行%s" % (strlong2, joink))

    t = threading.Timer(7200, check_op_jira)
    t.start()


t = threading.Timer(7200, check_op_jira)
t.start()
# Create your views here.
