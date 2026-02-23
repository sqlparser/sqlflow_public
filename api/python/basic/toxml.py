#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
import GenerateToken


def toxml(server, port, sql, dbvendor, userId, token):
    url = "/api/gspLive_backend/demo/xml/toXML"
    if 'api.gudusoft.com' in server:
        url = '/gspLive_backend/demo/xml/toXML'
    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url

    data = {'sql': sql, 'dbvendor': dbvendor, 'userId': userId, 'token': token}
    header_dict = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    try:
        r = requests.post(url, data=data, headers=header_dict, verify=False)
    except Exception as e:
        print('convert failed.', e)
    result = json.loads(r.text)

    usedTime = result['data']['usedTime']
    version = result['data']['gsp.version']
    if result['code'] == 200:
        xml = result['data']['xml']
        print('elapsed time: ' + usedTime+' ,gsp version: ' + version + ' ,xml result: ')
        print(xml)
    else:
        print('to xml failed. elapsed time: ' + usedTime + ' ,gsp version: ' + version + ' ,error info: ')
        print(result['error'])


if __name__ == '__main__':
    # the user id of sqlflow web or client, required true
    userId = ''

    # the secret key of sqlflow user for webapi request, required true
    screctKey = ''

    # sqlflow server, For the cloud version, the value is https://api.gudusoft.com
    server = 'https://api.gudusoft.com'

    # sqlflow api port, For the cloud version, the value is 80
    port = ''

    # The token is generated from userid and usersecret. It is used in every Api invocation.
    token = GenerateToken.getToken(userId, server, port, screctKey)

    # sql to be checked
    sql = 'select * from table1'

    # database type, dbvansi,dbvathena,dbvazuresql,dbvbigquery,dbvcouchbase,dbvdb2,dbvgreenplum,dbvgaussdb,dbvhana,dbvhive,dbvimpala,dbvinformix,dbvmdx,dbvmysql,dbvnetezza,dbvopenedge,dbvoracle,dbvpresto,dbvpostgresql,dbvredshift,dbvsnowflake,dbvmssql,dbvsparksql,dbvsybase,dbvteradata,dbvvertica
    dbvendor = 'dbvoracle'

    # to xml
    toxml(server, port, sql, dbvendor, userId, token)
