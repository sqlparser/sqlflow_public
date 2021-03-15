#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

import json
import sys
import os


def getResult(download, userId, token, server, port, jobId, filePath):
    sep = 'data' + os.sep + 'result' + os.sep
    filePath = filePath + '_' + jobId
    if download == '1':
        url = "/gspLive_backend/sqlflow/job/exportLineageAsJson"
        filePath = sep + filePath + '_json.json'
    elif download == '3':
        url = "/gspLive_backend/sqlflow/job/exportLineageAsGraphml"
        filePath = sep + filePath + '_graphml.graphml'
    elif download == '2':
        url = "/gspLive_backend/sqlflow/job/exportLineageAsCsv"
        filePath = sep + filePath + '_csv.csv'
    else:
        print('Please enter the correct output type.')
        sys.exit(0)

    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url

    data = {'jobId': jobId, 'token': token, 'userId': userId, 'tableToTable': 'false'}
    datastr = json.dumps(data)

    print('start download result to sqlflow.')
    try:
        response = requests.post(url, data=eval(datastr))
    except Exception:
        print('download result to sqlflow failed.')
        sys.exit(0)

    if not os.path.exists(sep):
        os.makedirs(sep)

    try:
        with open(filePath, 'wb') as f:
            f.write(response.content)
    except Exception:
        print(filePath, 'is not exist.')
        sys.exit(0)

    print('download result to sqlflow successful.file path is ', filePath)
