#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
import sys
import GenerateToken
import GenerateLineageParam


def getResult(server, port, data, files):
    url = "/api/gspLive_backend/sqlflow/generation/sqlflow/exportFullLineageAsCsv"
    if 'api.gudusoft.com' in server:
        url = '/gspLive_backend/sqlflow/generation/sqlflow/exportFullLineageAsCsv'
    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url

    datastr = json.dumps(data)

    print('start get csv result from sqlflow.')
    try:
        if files != '':
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
    server = 'http://127.0.0.1'

    # sqlflow api port, For the cloud version, the value is 80
    port = '8165'

    # For the cloud version
    # server = 'https://api.gudusoft.com'
    # port = '80'

    # The token is generated from userid and usersecret. It is used in every Api invocation.
    token = GenerateToken.getToken(userId, server, port, screctKey)

    # delimiter of the values in CSV, default would be ',' string
    delimiter = ','

    # export_include_table, string
    export_include_table = ''

    # showConstantTable, boolean
    showConstantTable = 'true'

    # Whether treat the arguments in COUNT function as direct Dataflow, boolean
    treatArgumentsInCountFunctionAsDirectDataflow = ''

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

    # sql text
    # sqltext = 'select * from table'
    # data = GenerateLineageParam.buildSqltextParam(userId, token, delimiter, export_include_table, showConstantTable, treatArgumentsInCountFunctionAsDirectDataflow, dbvendor, sqltext)
    # resp = getResult(server, port, data, '')
    
    # sql file
    sqlfile = 'test.sql'
    data, files = GenerateLineageParam.buildSqlfileParam(userId, token, delimiter, export_include_table,
                                                         showConstantTable,
                                                         treatArgumentsInCountFunctionAsDirectDataflow, dbvendor,
                                                         sqlfile)
    resp = getResult(server, port, data, files)
    print(resp)
