from django.shortcuts import render

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
    'server': 'http://192.168.60.68:8080',
    'verify': False,
}
jira = JIRA(options, basic_auth=('admin', 'AdminYwzx'))



def index(request):
    if request.method == 'POST':
        print("**********************************************")
        data = json.loads(request.body)
        print(data)
        keyname = data['issue']['fields']['project']['key']
        print("**********************************************")
        if keyname == 'YFZX':
            os.system("python /root/bot/yfzx/Script/yfzx.py [咖啡]【测试】有数据推送过来[咖啡]")
    return render(request, "index.html")

# Create your views here.
