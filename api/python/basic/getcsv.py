#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
import sys
import os
import zipfile


def getToken(userId, server, port, screctKey):
    if userId == 'gudu|0123456789':
        return 'token'
    url = '/api/gspLive_backend/user/generateToken'
    if 'api.gudusoft.com' in server:
        url = '/gspLive_backend/user/generateToken'
    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url
    mapA = {'secretKey': screctKey, 'userId': userId}
    header_dict = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        r = requests.post(url, data=mapA, headers=header_dict)
    except Exception as e:
        print('get token failed.', e)
    result = json.loads(r.text)

    if result['code'] == '200':
        return result['token']
    else:
        print(result['error'])


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


def getResult(userId, token, server, port, delimiter, export_include_table, showConstantTable,
              treatArgumentsInCountFunctionAsDirectDataflow, dbvendor, sqltext, sqlfile):
    url = "/api/gspLive_backend/sqlflow/generation/sqlflow/exportFullLineageAsCsv"
    if 'api.gudusoft.com' in server:
        url = '/gspLive_backend/sqlflow/generation/sqlflow/exportFullLineageAsCsv'
    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url

    files = ''
    if sqlfile != '':
        if os.path.isdir(sqlfile):
            print('The SQL file cannot be a directory.')
            sys.exit(0)
        files = {'sqlfile': open(sqlfile, 'rb')}

    data = {'dbvendor': dbvendor, 'token': token, 'userId': userId}
    if delimiter != '':
        data['delimiter'] = delimiter
    if export_include_table != '':
        data['export_include_table'] = export_include_table
    if showConstantTable != '':
        data['showConstantTable'] = showConstantTable
    if treatArgumentsInCountFunctionAsDirectDataflow != '':
        data['treatArgumentsInCountFunctionAsDirectDataflow'] = treatArgumentsInCountFunctionAsDirectDataflow
    if sqltext != '':
        data['sqltext'] = sqltext
    datastr = json.dumps(data)

    print('start get csv result from sqlflow.')
    try:
        if sqlfile != '':
            response = requests.post(url, data=eval(datastr), files=files)
        else:
            response = requests.post(url, data=eval(datastr))
    except Exception as e:
        print('get csv result from sqlflow failed.', e)
        sys.exit(0)

    print('get csv result from sqlflow successful. result : ')
    print()
    return response.text


if __name__ == '__main__':
    # the user id of sqlflow web or client, required true
    userId = ''

    # the secret key of sqlflow user for webapi request, required true
    screctKey = ''

    # sqlflow server, For the cloud version, the value is https://api.gudusoft.com
    server = ''

    # sqlflow api port, For the cloud version, the value is 80
    port = ''

    # The token is generated from userid and usersecret. It is used in every Api invocation.
    token = getToken(userId, server, port, screctKey)

    # delimiter of the values in CSV, default would be ',' string
    delimiter = ','

    # export_include_table, string
    export_include_table = ''

    # showConstantTable, boolean
    showConstantTable = 'true'

    # Whether treat the arguments in COUNT function as direct Dataflow, boolean
    treatArgumentsInCountFunctionAsDirectDataflow = ''

    # sql text
    sqltext = ''

    # sql file
    sqlfile = '/Users/chenbo/Documents/test.sql'

    # database type,
    # dbvazuresql
    # dbvbigquery
    # dbvcouchbase
    # dbvdb2
    # dbvgreenplum
    # dbvhana
    # dbvhive
    # dbvimpala
    # dbvinformix
    # dbvmdx
    # dbvmysql
    # dbvnetezza
    # dbvopenedge
    # dbvoracle
    # dbvpostgresql
    # dbvredshift
    # dbvsnowflake
    # dbvmssql
    # dbvsparksql
    # dbvsybase
    # dbvteradata
    # dbvvertica
    dbvendor = 'dbvoracle'

    resp = getResult(userId, token, server, port, delimiter, export_include_table, showConstantTable,
                     treatArgumentsInCountFunctionAsDirectDataflow, dbvendor, sqltext, sqlfile)
    print(resp)
