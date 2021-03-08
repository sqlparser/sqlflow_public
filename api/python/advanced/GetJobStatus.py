#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

import json
import sys


def getStatus(userId, token, server, port, jobId):
    url = "/gspLive_backend/sqlflow/job/displayUserJobSummary"

    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url

    data = {'jobId': jobId, 'token': token, 'userId': userId}
    datastr = json.dumps(data)

    try:
        response = requests.post(url, data=eval(datastr))
    except Exception:
        print('get job status to sqlflow failed.')
        sys.exit(0)

    result = json.loads(response.text)
    if result['code'] == 200:
        status = result['data']['status']
        if status == 'fail':
            print(result['data']['errorMessage'])
            sys.exit(0)
        return status
