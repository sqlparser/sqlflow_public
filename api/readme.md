## How to use Rest API of SQLFlow

This article describes how to use the Rest API provided by the SQLFlow to 
communicate with the SQLFlow server and get the generated metadata and data lineage.

In this article, we use `Curl` to demonstrate the usage of the Rest API, 
you can use any preferred programming language as you like.

### Prerequisites
To use the Rest API of the SQLFlow, you need to <a href="https://gudusoft.com">obtain a premium account</a>. 
After that, you will get the `userid` and `secret key`, which will be used in the API.

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
curl -X POST "https://api.gudusoft.com/gspLive_backend/user/generateToken" -H  "Request-Origion:testClientDemo" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:application/x-www-form-urlencoded;charset=UTF-8" -d "secretKey=YOUR SECRET KEY" -d "userId=YOUR USER ID HERE"
```


#### 2. Generate the data lineage

Call this API by sending the SQL query and get the result includes the data lineage.

```
/gspLive_backend/sqlflow/generation/sqlflow
```

Example in `Curl`
```
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow?showRelationType=fdd" -H  "Request-Origion:testClientDemo" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:multipart/form-data" -F "sqlfile=" -F "dbvendor=dbvoracle" -F "ignoreRecordSet=false" -F "simpleOutput=false" -F "sqltext=CREATE VIEW vsal  as select * from emp" -F "userId=YOUR USER ID HERE"  -F "token=YOUR TOKEN HERE"
```

#### 3. Generate the data lineage csv result

Call this API by sending the SQL file and get the csv result includes the data lineage.

```
/gspLive_backend/sqlflow/generation/sqlflow/exportLineageAsCsv
```

```
curl -X POST https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow/exportLineageAsCsv" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:multipart/form-data" -F "userId=YOUR USER ID HERE" -F "token=YOUR TOKEN HERE" -F "dbvendor=dbvoracle" -F "showRelationType=fdd" -F "sqlfile=@YOUR UPLOAD FILE PATH HERE" --output YOUR DOWNLOAD FILE PATH HERE
```

**Note:**
 * -H  "Content-Type:multipart/form-data" is must required.
 * Add **@** before the upload file path 
 * --output is must required, and the download file is a **zip** file.


#### 4.  Other features
You can also use the rest API to submit a zip file that includes many SQL files or generate a map of the columns in the join condition.

### The full reference to the Rest APIs

[SQLFlow rest API reference](sqlflow_api.md)
