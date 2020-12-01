## How to use Rest API of SQLFlow

Thiis article describles how to use the Rest API provided by the SQLFlow to 
communicate with the SQLFlow server and get the genereated metadata and data lineage.

In this article, we use `Curl` to demonstrate the usage of the Rest API, 
you can use any preferred programming language as you like.

### Prerequisites
In order to use the Rest API of the SQLFlow, you need to <a href="https://gudusoft.com">obtain a premium account</a>. 
After that, you will get the `userid` and `secret key` which will be used in the API.

- User ID
- Secrete Key

### Call Rest API

#### 1. Generate a token

Once you have the `userid` and `secret key`, the first API need to call is:

```
/gspLive_backend/user/generateToken
```

This API will return a temporary token that needs to be used in the API call thereafter.

```
curl -X POST "https://api.gudusoft.com/gspLive_backend/user/generateToken" -H  "Request-Origion:testClientDemo" -H  "accept:application/json;charset=utf-8" -H  "Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJ0ZXN0IiwiZXhwIjoxNjMwOTQ0MDAwLCJpYXQiOjE1OTkzMjE2MDB9._2kef0EnD-ASoDsolmoV0BcPIjr9pREHsn4n01XdKaE" -H  "Content-Type:application/x-www-form-urlencoded;charset=UTF-8" -d "secretKey=YOUR SECRET KEY" -d "userId=YOUR USER ID HERE"
```


#### 2. Generate the data lineage

Call this API by sending the SQL query and get the result including the data lineage.

```
/gspLive_backend/sqlflow/generation/sqlflow
```

Example in `Curl`
```
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow?showRelationType=fdd" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:application/json;charset=utf-8" -H  "Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJ0ZXN0IiwiZXhwIjoxNjMwOTQ0MDAwLCJpYXQiOjE1OTkzMjE2MDB9._2kef0EnD-ASoDsolmoV0BcPIjr9pREHsn4n01XdKaE" -H  "Content-Type:multipart/form-data" -F "sqlfile=" -F "dbvendor=dbvoracle" -F "userId=YOUR USER ID HERE" -F "ignoreRecordSet=false" -F "simpleOutput=false" -F "sqltext=CREATE VIEW vsal  as select * from emp" -F "token=YOUR TOKEN HERE"
```

### The full reference to the Rest APIs

[SQLFlow rest API reference](sqlflow_api.md)
