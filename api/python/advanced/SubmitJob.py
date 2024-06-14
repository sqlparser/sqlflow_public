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

    if isinstance(sqlfiles, str):
        if os.path.isdir(sqlfiles):
            sqlfiles = [sqlfiles]
        else:
            sqlfiles = [sqlfiles]

    if isinstance(sqlfiles, list):
        sqlfiles_zip = toZip(sqlfiles)

    files = {'sqlfiles': open(sqlfiles_zip, 'rb')}
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


def toZip(file_list):
    zip_filename = 'files.zip'

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as z:
        for file in file_list:
            if os.path.isfile(file):
                z.write(file, os.path.basename(file))
            elif os.path.isdir(file):
                for dir_path, dir_names, filenames in os.walk(file):
                    for filename in filenames:
                        z.write(os.path.join(dir_path, filename), os.path.join(os.path.basename(file), filename))

    return zip_filename
