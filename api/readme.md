## How to use the Rest API of SQLFlow

This article describes how to use the Rest API provided by the SQLFlow to 
communicate with the SQLFlow server and get the generated metadata and data lineage.

In this article, we use `Curl` to demonstrate the usage of the Rest API, 
you can use any preferred programming language as you like.

### Prerequisites
In order to use the SQLFlow rest API, you may connect to the [SQLFlow Cloud server](https://sqlflow.gudusoft.com),
Or, setup a [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/) on your owner server.

1. SQLFlow Cloud server

- User ID
- Secrete Key

If you want to connect to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com), you may [request a 30 days premium account](https://www.gudusoft.com/request-a-premium-account/) to 
[get the necessary userId and secret code](/sqlflow-userid-secret.md).


2. SQLFlow on-premise version

Please [check here](https://github.com/sqlparser/sqlflow_public/blob/master/install_sqlflow.md) to see how to install SQLFlow on-premise version on you own server.

- User ID
- Secrete Key

Always set userId to `gudu|0123456789` and keep `userSecret` empty when connect to the SQLFlow on-premise version.


### Difference of the API calls between SQLFlow Cloud server and SQLFlow on-premise version

1. TOKEN is not needed in the API calls when connect to the SQLFlow on-premise version
2. userId alwyas set to `gudu|0123456789` and `userSecret` leave empty when connect to the SQLFlow on-premise version.
3. The server port is 8081 by default for the SQLFlow on-premise version, and There is no need to specify the port when connect to the SQLFlow Cloud server.

Regarding the server port of the SQLFlow on-premise version, please [check here](https://github.com/sqlparser/sqlflow_public/tree/master/grabit#1-sqlflow-server) for more information.



### Using the Rest API

#### 1. Generate a token


Once you have the `userid` and `secret key`, the first API need to call is:

```
/gspLive_backend/user/generateToken
```

This API will return a temporary token that needs to be used in the API call thereafter.

**SQLFlow Cloud Server**
```
curl -X POST "https://api.gudusoft.com/gspLive_backend/user/generateToken" -H  "Request-Origion:testClientDemo" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:application/x-www-form-urlencoded;charset=UTF-8" -d "secretKey=YOUR SECRET KEY" -d "userId=YOUR USER ID HERE"
```

**SQLFlow on-premise version**

TOKEN is not needed in the on-premise version. So, there is no need to generate a token.


#### 2. Generate the data lineage

Call this API by sending the SQL query and get the result includes the data lineage.

```
/gspLive_backend/sqlflow/generation/sqlflow
```


**SQLFlow Cloud Server**
```
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow?showRelationType=fdd" -H  "Request-Origion:testClientDemo" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:multipart/form-data" -F "sqlfile=" -F "dbvendor=dbvoracle" -F "ignoreRecordSet=false" -F "simpleOutput=false" -F "sqltext=CREATE VIEW vsal  as select * from emp" -F "userId=YOUR USER ID HERE"  -F "token=YOUR TOKEN HERE"
```

**SQLFlow on-premise version**
```
curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/generation/sqlflow?showRelationType=fdd"    -H  "Request-Origion:testClientDemo" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:multipart/form-data" -F "sqlfile=" -F "dbvendor=dbvoracle" -F "ignoreRecordSet=false" -F "simpleOutput=false" -F "sqltext=CREATE VIEW vsal  as select * from emp" -F "userId=gudu|0123456789" 
```


#### 3. Export the data lineage in csv format

Call this API by sending the SQL file and get the csv result includes the data lineage.

```
/gspLive_backend/sqlflow/generation/sqlflow/exportLineageAsCsv
```

```
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow/exportLineageAsCsv" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:multipart/form-data" -F "userId=YOUR USER ID HERE" -F "token=YOUR TOKEN HERE" -F "dbvendor=dbvoracle" -F "showRelationType=fdd" -F "sqlfile=@YOUR UPLOAD FILE PATH HERE" --output YOUR DOWNLOAD FILE PATH HERE
```

Sample:
```
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow/exportLineageAsCsv" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:multipart/form-data" -F "userId=auth0|5fc8e95991a780006f180d4d" -F "token=YOUR TOKEN HERE" -F "dbvendor=dbvoracle" -F "showRelationType=fdd" -F "sqlfile=@c:\prg\tmp\demo.sql" --output c:\prg\tmp\demo.csv
```


**Note:**
 * -H  "Content-Type:multipart/form-data" is required.
 * Add **@** before the upload file path 
 * --output is required.
 * Optional, if you just want to fetch table to table relations, please add **-F "tableToTable=true"**


#### 4.  Submit multiple SQL files and get the data lineage in CSV, JSON, graphml format.
<a href="sqlflow-job-api-tutorial.md">Rest APIs: Job</a>

### The full reference to the Rest APIs

[SQLFlow rest API reference](sqlflow_api.md)

### Troubleshooting

- Under windows, you may need to add option `--ssl-no-revoke` to avoid some security issues, `curl --ssl-no-revoke`
