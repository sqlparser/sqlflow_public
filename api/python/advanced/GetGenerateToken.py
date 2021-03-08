#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

import json


def getToken(sys, userId, server, port):
    if len(sys.argv) < 1:
        print('Please enter the args.')
        sys.exit(0)

    url = '/gspLive_backend/user/generateToken'
    screctKey = ''
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '/k':
            try:
                if sys.argv[i + 1] is not None:
                    screctKey = sys.argv[i + 1]
            except Exception:
                print(
                    'Please enter the screctKey，the secret key of sqlflow user for webapi request, required true. eg: /k xxx')
                sys.exit(0)

    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url
    mapA = {'secretKey': screctKey, 'userId': userId}
    header_dict = {"Content-Type": "application/x-www-form-urlencoded"}

    print('start get token.')
    try:
        r = requests.post(url, data=mapA, headers=header_dict)
    except Exception:
        print('get token failed.')
        sys.exit(0)
    result = json.loads(r.text)

    if result['code'] == '200':
        print('get token successful.')
        return result['token']
    else:
        print(result['error'])
        sys.exit(0)
