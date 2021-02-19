#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

import json
import sys


def toSqlflow(userId, token, server, port, jobName, dbvendor, sqlfiles):
    url = '/gspLive_backend/sqlflow/job/submitUserJob'

    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url

    files = {'sqlfiles': open(sqlfiles, 'rb')}
    data = {'dbvendor': dbvendor, 'jobName': jobName, 'token': token, 'userId': userId}
    datastr = json.dumps(data)

    print('start submit job to sqlflow.')
    try:
        response = requests.post(url, data=eval(datastr), files=files)
    except Exception:
        print('submit job to sqlflow failed.')
        sys.exit(0)

    result = json.loads(response.text)

    if result['code'] == 200:
        print('submit job to sqlflow successful.')
        return result['data']['jobId']
    else:
        print(result['error'])
        sys.exit(0)
