#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import GetGenerateToken
import SubmitJob
import time
import GetResultToSqlflow
import GetJobStatus
import datetime

if __name__ == '__main__':

    print('========================================grabit-python======================================')

    # sqlflow platform user id. If the on-permise version is used, the default value is gudu|0123456789
    userId = ''

    # Type of database to analyze, for example: oracle,mysql,mssql...
    dbvendor = ''

    # File or directory path to analyze
    sqlfiles = ''

    # sqlflow server
    server = ''

    # sqlflow api prot,the default value is 8081
    port = ''

    # Analysis result return type. The value is optional: json, csv, graphml
    downloadFileType = ''

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '/u':
            try:
                if sys.argv[i + 1] is not None:
                    userId = sys.argv[i + 1]
                else:
                    print(
                        'Please enter the userId，the user id of sqlflow web or client, required true. eg: /n gudu|123456789')
                    sys.exit(0)
            except BrokenPipeError:
                print(
                    'Please enter the userId，the user id of sqlflow web or client, required true. eg: /n gudu|123456789')
        if sys.argv[i] == '/t':
            try:
                if sys.argv[i + 1] is not None:
                    dbvendor = sys.argv[i + 1]
                else:
                    print(
                        'Please enter the dbvendor.')
                    sys.exit(0)
            except Exception:
                print(
                    'Please enter the dbvendor.')
        if sys.argv[i] == '/f':
            try:
                if sys.argv[i + 1] is not None:
                    sqlfiles = sys.argv[i + 1]
                else:
                    print(
                        'Please enter the sqlfiles，request sql files, please use multiple parts to submit the sql files, required true. eg: /f path')
                    sys.exit(0)
            except Exception:
                print(
                    'Please enter the sqlfiles，request sql files, please use multiple parts to submit the sql files, required true. eg: /f path')
        if sys.argv[i] == '/s':
            try:
                if sys.argv[i + 1] is not None:
                    server = sys.argv[i + 1]
                else:
                    print('Please enter the server. eg: /s https://api.gudusoft.com or /s https://127.0.0.1')
                    sys.exit(0)
            except Exception:
                print('Please enter the server. eg: /s https://api.gudusoft.com or /s https://127.0.0.1')
                sys.exit(0)
        if sys.argv[i] == '/p':
            try:
                if sys.argv[i + 1] is not None:
                    port = sys.argv[i + 1]
            except Exception:
                print('Please enter the port. eg: /p 8081')
                sys.exit(0)
        if sys.argv[i] == '/r':
            try:
                if sys.argv[i + 1] is not None:
                    downloadFileType = sys.argv[i + 1]
            except Exception:
                print('Please enter the download type to sqlflow, type json csv diagram : eg: /r 1')
                sys.exit(0)

    if userId == '':
        print('Please enter the userId，the user id of sqlflow web or client, required true. eg: /n gudu|123456789')
        sys.exit(0)
    if dbvendor == '':
        print(
            'Please enter the dbvendor，available values:bigquery,couchbase,db2,greenplum,hana,hive,impala,informix,mdx,mysql,netezza,openedge,oracle,postgresql,redshift,snowflake,mssql,sybase,teradata,vertica. eg: /t oracle')
        sys.exit(0)

    if dbvendor == 'mssql' or dbvendor == 'sqlserver':
        dbvendor = 'mssql'

    dbvendor = 'dbv' + dbvendor

    if sqlfiles == '':
        print(
            'Please enter the sqlfiles，request sql files, please use multiple parts to submit the sql files, required true. eg: /f path')
        sys.exit(0)
    if server == '':
        print('Please enter the server. eg: /s https://api.gudusoft.com or /s https://127.0.0.1')
        sys.exit(0)

    if server.find('http:') == -1 and server.find('https:') == -1:
        server = 'http://' + server

    if server.endswith(os.sep):
        server = server[:-1]

    if server == 'https://sqlflow.gudusoft.com':
        server = 'https://api.gudusoft.com'

    if userId == 'gudu|0123456789':
        token = 'token'
    else:
        token = GetGenerateToken.getToken(sys, userId, server, port)

    time_ = datetime.datetime.now().strftime('%Y%m%d')

    jobId = SubmitJob.toSqlflow(userId, token, server, port, time_, dbvendor, sqlfiles)

    if downloadFileType != '':
        while True:
            status = GetJobStatus.getStatus(userId, token, server, port, jobId)
            if status == 'partial_success' or status == 'success':
                GetResultToSqlflow.getResult(downloadFileType, userId, token, server, port, jobId, time_)
                break

    print('========================================grabit-python======================================')

    sys.exit(0)
