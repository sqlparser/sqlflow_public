#!/usr/bin/python
# -*- coding: UTF-8 -*-
import zipfile

import requests

import json
import sys
import os


def toSqlflow(userId, token, server, port, jobName, dbvendor, sqlfiles):
    url = '/gspLive_backend/sqlflow/job/submitUserJob'

    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url

    if os.path.isdir(sqlfiles):
        sqlfiles = toZip(sqlfiles)
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


def toZip(start_dir):
    if start_dir.endswith(os.sep):
        start_dir = start_dir[:-1]
    start_dir = start_dir
    file_news = start_dir + '.zip'

    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        f_path = dir_path.replace(start_dir, '')
        f_path = f_path and f_path + os.sep or ''
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path + filename)
    z.close()
    return file_news
