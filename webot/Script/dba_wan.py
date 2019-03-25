#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import json
import sys
import logging

Toparty = '6'
agentid = 1000003
corpid = 'xxxxxxxxxxxxxxxx'
corpsecret = 'xxxxxxxxxxxxxxxx'
url = 'https://qyapi.weixin.qq.com'
subject = sys.argv[1]
message = ' '
logging.basicConfig(level=logging.DEBUG, filename='E:\Python_project\Scripts\my.log',
                    format='%(asctime)s - %(levelname)s')


class Weixin:
    def __init__(self, url, corpid, corpsecret):
        token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
        self.token = json.loads(urllib.request.urlopen(token_url).read().decode())['access_token']

    def send_message(self, url, data):
        send_url = '%s/cgi-bin/message/send?access_token=%s' % (url, self.token)
        self.respone = urllib.request.urlopen(urllib.request.Request(url=send_url, data=data)).read()
        x = json.loads(self.respone.decode())['errcode']

        if x == 0:
            logging.debug('Successfully %s    %s' % (subject,message))
            return 'Succesfully'
        else:
            logging.debug('Failed %s    %s' % (subject,message))
            return 'Failed'

    def messages(self, subject):
        values = {
            "toparty": Toparty,
            "msgtype": 'text',
            "agentid": agentid,
            "text": {'content': subject},
            "safe": 0
        }
        return self.send_message(url, bytes(json.dumps(values), 'utf-8'))


if __name__ == '__main__':
    obj = Weixin(url, corpid, corpsecret)
    ret = obj.messages(subject)
