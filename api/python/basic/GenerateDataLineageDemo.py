import requests

import json

if __name__ == '__main__':
    tokenUrl = 'https://api.gudusoft.com/gspLive_backend/user/generateToken'
    generateDataLineageUrl = 'https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow'

    # the user id of sqlflow web or client, required true
    userId = ''

    # the secret key of sqlflow user for webapi request, required true
    screctKey = ''

    # sql file, required false
    sqlfile = ''

    # sql text, required false
    sqltext = ''

    # whether ignore the record set, required false, default value is false
    ignoreRecordSet = False

    # database vendor, required true, available values:
    # dbvbigquery, dbvcouchbase,dbvdb2,dbvgreenplum,dbvhana,dbvhive,dbvimpala,dbvinformix,dbvmdx,dbvmysql,
    # dbvnetezza,dbvopenedge,dbvoracle,dbvpostgresql,dbvredshift,dbvsnowflake,dbvmssql,dbvsybase,dbvteradata,dbvvertica
    dbvendor = ''

    # show relation type, required false, default value is fdd, multiple values seperated by comma like fdd,frd,fdr
    # Available values:
    # fdd: value of target column from source column
    # frd: the recordset count of target column which is affect by value of source column
    # fdr: value of target column which is affected by the recordset count of source column
    # join: combine rows from two or more tables, based on a related column between them

    showRelationType = 'fdd'

    # whether simple output relation, required false, default value is false
    simpleOutput = False
    false = False

    mapA = {'secretKey': screctKey, 'userId': userId}
    header_dict = {"Content-Type": "application/x-www-form-urlencoded; charset=utf8"}
    r = requests.post(tokenUrl, data=mapA, headers=header_dict)
    rs = eval(r.text)
    print(rs)

    tk = rs.get("token")

    if not sqlfile is None and sqlfile is not '':
        files = {'sqlfile': open(sqlfile, 'rb')}
        data = {'dbvendor': dbvendor, 'ignoreRecordSet': ignoreRecordSet, 'simpleOutput': simpleOutput,
                'showRelationType': showRelationType, 'token': tk,
                'userId': userId}
        datastr = json.dumps(data)
        response = requests.post(generateDataLineageUrl, data=eval(datastr), files=files)

        jsonStr = response.json()
        print(jsonStr)
    elif not sqltext is None and sqltext is not '':
        data = {'dbvendor': dbvendor, 'ignoreRecordSet': ignoreRecordSet, 'simpleOutput': simpleOutput,
                'showRelationType': showRelationType, 'token': tk,
                'userId': userId, 'sqltext': sqltext}
        datastr = json.dumps(data)
        response = requests.post(generateDataLineageUrl, data=eval(datastr))

        jsonStr = response.json()
        print(jsonStr)
    else:
        print("Please set sqltext or sqlfile")
