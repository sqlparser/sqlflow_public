# SQLFlow WebAPI

## JWT WEB Authorization (Only for sqlflow web)
* All of the restful requests are based on JWT authorization. Before accessing the sqlflow WebAPI, web user needs to obtain the corresponding JWT token for legal access.
* How to use JWT Token for security authentication?
  * In the header of the HTTP request, please pass the parameters:
   ```
     Key:      Authorization
     Value:    Token <token>
  ```
  
## JWT Client API Authorization (for sqlflow client api call)
* All of the restful requests are based on JWT authorization. Before accessing the sqlflow WebAPI, client user needs to obtain the corresponding JWT token for legal access.

* How to get JWT Token
  1. Login on the sqlflow web
  2. Move mouse on the login user image, click the "generate token" menu item, you can get the user secret key and token, the ttl of token is 24 hours.
  3. When you get the user secret key, you can call **/gspLive_backend/user/generateToken** api to refresh token, the ttl of new token is 24 hours.
  4. **/gspLive_backend/user/generateToken**
       * **userId**: the user id of sqlflow web or client, required **true** 
       * **secretKey**: the secret key of sqlflow user for webapi request, required **true** 

* How to use JWT Token for security authentication?
  * Each webapi contains two parameters, named userId and token.

## WebAPI

### Sqlflow Generation Interface  

* **/sqlflow/generation/sqlflow**
  * Description: generate sqlflow model
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true
    * sqltext: sql text, required false
    * sqlfile: sql file, required false
    * **dbvendor**: database vendor, required **true**, available values: 
      * dbvbigquery, dbvcouchbase,dbvdb2,dbvgreenplum,dbvhana,dbvhive,dbvimpala,dbvinformix,dbvmdx,dbvmysql,dbvnetezza,dbvopenedge,dbvoracle,dbvpostgresql,dbvredshift,dbvsnowflake,dbvmssql,dbvsybase,dbvteradata,dbvvertica
    * showRelationType: show relation type, required false, default value is **fdd**, multiple values seperated by comma like fdd,frd,fdr. Available values: 
      * **fdd**: value of target column from source column
      * **frd**: the recordset count of target column which is affect by value of source column
      * **fdr**: value of target column which is affected by the recordset count of source column
      * **join**: combine rows from two or more tables, based on a related column between them
    * simpleOutput: whether simple output relation, required false, default value is false
    * ignoreRecordSet: whether ignore the record set, required false, default value is false
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message. 
  * Sample:
    * test sql:
    ```sql
      select name from user
    ```
    * curl command:
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/generation/sqlflow" -H "accept:application/json;charset=utf-8" -F "userId=google-oauth2|104002923119102769706"  -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE" -F  "dbvendor=dbvoracle" -F "ignoreRecordSet=true" -F "sqltext=select name from user"
    ```
    * response: 
    ```json
      {
        "code": 200,
        "data": {
          "dbvendor": "dbvoracle",
          "dbobjs": [
            ...
          ],
          "relations": [
            ...
          ]
        },
        "sessionId": "6172a4095280ccce97e996242d8b4084f46e2c954455e71339aeffccad5f0d57_1599501108040"
      }
    ```
    
* **/sqlflow/generation/sqlflow/graph**
  * Description: generate sqlflow model and graph
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true
    * sqltext: sql text, required false
    * sqlfile: sql file, required false
    * **dbvendor**: database vendor, required **true**, available values: 
      * dbvbigquery, dbvcouchbase,dbvdb2,dbvgreenplum,dbvhana,dbvhive,dbvimpala,dbvinformix,dbvmdx,dbvmysql,dbvnetezza,dbvopenedge,dbvoracle,dbvpostgresql,dbvredshift,dbvsnowflake,dbvmssql,dbvsybase,dbvteradata,dbvvertica
    * showRelationType: show relation type, required false, default value is **fdd**, multiple values seperated by comma like fdd,frd,fdr. Available values:
      * **fdd**: value of target column from source column
      * **frd**: the recordset count of target column which is affect by value of source column
      * **fdr**: value of target column which is affected by the recordset count of source column
      * **join**: combine rows from two or more tables, based on a related column between them
    * simpleOutput: whether output relation simply, required false, default value is false
    * ignoreRecordSet: whether ignore the record sets, required false, default value is false  
    * showLinkOnly: whether show relation linked columns only, required false, default value is true 
    * hideColumn: whether hide the column ui, required false, default value is false 
    * ignoreFunction: whether ignore the function relations, required false, default value is false 
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.  
  * Sample:
    * test sql:
    ```sql
      select name from user
    ```
    * curl command:
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/generation/sqlflow/graph" -H "accept:application/json;charset=utf-8" -F "userId=google-oauth2|104002923119102769706" -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE" -F "dbvendor=dbvoracle" -F "ignoreFunction=true" -F "ignoreRecordSet=true" -F "sqltext=select name from user"
    ```
    * response: 
    ```json
     {
       "code": 200,
       "data": {
         "mode": "global",
         "summary": {
           ...
         },
         "sqlflow": {
           "dbvendor": "dbvoracle",
           "dbobjs": [
               ...
           ]
         },
         "graph": {
           "elements": {
             "tables": [
               ...
             ],
             "edges": [
               ...
             ]
           },
           "tooltip": {},
           "relationIdMap": {
             ...
           },
           "listIdMap": {
             ...
           }
         }
       },
       "sessionId": "6172a4095280ccce97e996242d8b4084f46e2c954455e71339aeffccad5f0d57_1599501562051"
     }
    ```    
    
* **/sqlflow/generation/sqlflow/selectedgraph**          
  * Description: generate sqlflow model and selected dbobject graph
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true  
    * **sessionId**: request sessionId, the value is from api **/sqlflow/generation/sqlflow/graph**, required **true**
    * database: selected database, required false
    * schema: selected schema, required false
    * table: selected table, required false
    * isReturnModel: whether return the sqlflow model, required false, default value is true
    * **dbvendor**: database vendor, required **true**, available values: 
      * dbvbigquery, dbvcouchbase,dbvdb2,dbvgreenplum,dbvhana,dbvhive,dbvimpala,dbvinformix,dbvmdx,dbvmysql,dbvnetezza,dbvopenedge,dbvoracle,dbvpostgresql,dbvredshift,dbvsnowflake,dbvmssql,dbvsybase,dbvteradata,dbvvertica
    * showRelationType: show relation type, required false, default value is **fdd**, multiple values seperated by comma like fdd,frd,fdr. Available values: 
      * **fdd**: value of target column from source column
      * **frd**: the recordset count of target column which is affect by value of source column
      * **fdr**: value of target column which is affected by the recordset count of source column
      * **join**: combine rows from two or more tables, based on a related column between them
    * simpleOutput: whether output relation simply, required false, default value is false
    * ignoreRecordSet: whether ignore the record sets, required false, default value is false  
    * showLinkOnly: whether show relation linked columns only, required false, default value is true 
    * hideColumn: whether hide the column ui, required false, default value is false 
    * ignoreFunction: whether ignore the function relations, required false, default value is false 
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.
  * Sample:    
    * test sql:
    ```sql
      select name from user
    ```
    * session id: `6172a4095280ccce97e996242d8b4084f46e2c954455e71339aeffccad5f0d57_1599501562051`
    * curl command:
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/generation/sqlflow/selectedgraph" -H "accept:application/json;charset=utf-8" -F "userId=google-oauth2|104002923119102769706" -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE" -F "dbvendor=dbvoracle" -F "ignoreFunction=true" -F "ignoreRecordSet=true" -F "isReturnModel=false" -F "sessionId=6172a4095280ccce97e996242d8b4084f46e2c954455e71339aeffccad5f0d57_1599501562051" -F "table=user"

    ```
    * response: 
    ```json
     {
       "code": 200,
       "data": {
         "mode": "global",
         "summary": {
           ...
         },
         "graph": {
           "elements": {
             "tables": [
               ...
             ],
             "edges": [
               ...
             ]
           },
           "tooltip": {},
           "relationIdMap": {
             ...
           },
           "listIdMap": {
             ...
           }
         }
       },
       "sessionId": "6172a4095280ccce97e996242d8b4084f46e2c954455e71339aeffccad5f0d57_1599501562051"
     }
    ``` 
* **/sqlflow/generation/sqlflow/getSelectedDbObjectInfo**          
  * Description: get the selected dbobject information, such as file information, sql index, dbobject positions, sql which contains selected dbobject.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true  
    * **sessionId**: request sessionId, the value is from api **/sqlflow/generation/sqlflow/graph**, required **true**
    * **coordinates**: the select dbobject positions, it's a json array string, the value is from api **/sqlflow/generation/sqlflow/graph**, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.
  * Sample:    
    * test sql:
    ```sql
      select name from user
    ```
    * session id: `6172a4095280ccce97e996242d8b4084f46e2c954455e71339aeffccad5f0d57_1599501562051`
    * coordinates: `[{'x':1,'y':8,'hashCode':'3630d5472af5f149fe3fb2202c8a338d'},{'x':1,'y':12,'hashCode':'3630d5472af5f149fe3fb2202c8a338d'}]`
    * curl command:
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/generation/sqlflow/getSelectedDbObjectInfo" -H "accept:application/json;charset=utf-8" -F "userId=google-oauth2|104002923119102769706" -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE" -F "coordinates=[{'x':1,'y':8,'hashCode':'3630d5472af5f149fe3fb2202c8a338d'},{'x':1,'y':12,'hashCode':'3630d5472af5f149fe3fb2202c8a338d'}]" -F "sessionId=6172a4095280ccce97e996242d8b4084f46e2c954455e71339aeffccad5f0d57_1599501562051"
    ```
    * response: 
    ```json
      {
        "code": 200,
        "data": [
          {
            "index": 0,
            "positions": [
              {
                "x": 1,
                "y": 8
              },
              {
                "x": 1,
                "y": 12
              }
            ],
            "sql": "select name from user"
          }
        ]
      }
    ```    
    
### Sqlflow User Job Interface
* **/sqlflow/job/submitUserJob**
  * Description: submit user job for multiple sql files, support zip file.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true
    * **jobName**: job name, required **true**
    * **dbvendor**: database vendor, required **true**, available values: 
      * dbvbigquery, dbvcouchbase,dbvdb2,dbvgreenplum,dbvhana,dbvhive,dbvimpala,dbvinformix,dbvmdx,dbvmysql,dbvnetezza,dbvopenedge,dbvoracle,dbvpostgresql,dbvredshift,dbvsnowflake,dbvmssql,dbvsybase,dbvteradata,dbvvertica
    * **sqlfiles**:  request sql files, please use **multiple parts** to submit the sql files, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.  
  * Sample:
    * test sql file: D:\sql.txt
    * curl command:  **Note: please add **@** before the sql file path**
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/job/submitUserJob" -H "accept:application/json;charset=utf-8" -H "Content-Type:multipart/form-data" -F "userId=google-oauth2|104002923119102769706" -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE" -F "sqlfiles=@D:/sql.txt" -F "dbvendor=dbvoracle" -F "jobName=job_test"
    ```
    * response: 
    ```json
      {
        "code": 200,
        "data": {
          "jobId": "6218721f092540c5a771ca8f82986be7",
          "jobName": "job_test",
          "userId": "user_test",
          "dbVendor": "dbvoracle",
          "defaultDatabase": "",
          "defaultSchema": "",
          "fileNames": [
            "sql.txt"
          ],
          "createTime": "2020-09-08 10:11:28",
          "status": "create"
        }
      }
    ```    
    
* **/sqlflow/job/displayUserJobsSummary**        
  * Description: get the user jobs summary information.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message. 
  * Sample:
    * test sql file: D:\sql.txt
    * curl command: 
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/job/displayUserJobsSummary" -H "accept:application/json;charset=utf-8" -F "userId=google-oauth2|104002923119102769706" -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE"
    ```
    * response: 
    ```json
      {
        "code": 200,
        "data": {
          "total": 1,
          "success": 1,
          "partialSuccess": 0,
          "fail": 0,
          "jobIds": [
            "bb996c1ee5b741c5b4ff6c2c66c371dd"
          ],
          "jobDetails": [
            {
              "jobId": "bb996c1ee5b741c5b4ff6c2c66c371dd",
              "jobName": "job_test",
              "userId": "user_test",
              "dbVendor": "dbvoracle",
              "fileNames": [
                "sql.txt"
              ],
              "createTime": "2020-09-08 10:16:11",
              "status": "success",
              "sessionId": "a9f751281f8ef6936c554432e169359190d392565208931f201523e08036109d_1599531372233"
            }
          ]
        }
      }
    ```       
    
* **/sqlflow/job/displayUserJobSummary**        
  * Description: get the specify user job information.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true
    * **jobId**: job id, the value is from user jobs summary detail, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.  
  * Sample:
    * test sql file: D:\sql.txt
    * job id: bb996c1ee5b741c5b4ff6c2c66c371dd
    * curl command: 
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/job/displayUserJobSummary" -H "accept:application/json;charset=utf-8" -F "userId=google-oauth2|104002923119102769706" -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE" -F "jobId=bb996c1ee5b741c5b4ff6c2c66c371dd"
    ```
    * response: 
    ```json
      {
        "code": 200,
        "data": {
          "total": 1,
          "success": 1,
          "partialSuccess": 0,
          "fail": 0,
          "jobIds": [
            "bb996c1ee5b741c5b4ff6c2c66c371dd"
          ],
          "jobDetails": [
            {
              "jobId": "bb996c1ee5b741c5b4ff6c2c66c371dd",
              "jobName": "job_test",
              "userId": "user_test",
              "dbVendor": "dbvoracle",
              "fileNames": [
                "sql.txt"
              ],
              "createTime": "2020-09-08 10:16:11",
              "status": "success",
              "sessionId": "a9f751281f8ef6936c554432e169359190d392565208931f201523e08036109d_1599531372233"
            }
          ]
        }
      }
    ```      
    
* **/sqlflow/job/deleteUserJob**
  * Description: delete the user job by job id.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true
    * **jobId**: job id, the value is from user job detail, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message. 
  * Sample:
    * test sql file: D:\sql.txt
    * job id: bb996c1ee5b741c5b4ff6c2c66c371dd
    * curl command: 
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/job/deleteUserJob" -H "accept:application/json;charset=utf-8" -F "userId=google-oauth2|104002923119102769706" -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE" -F "jobId=bb996c1ee5b741c5b4ff6c2c66c371dd"
    ```
    * response: 
    ```json
      {
        "code": 200,
        "data": {
          "jobId": "bb996c1ee5b741c5b4ff6c2c66c371dd",
          "jobName": "job_test",
          "userId": "user_test",
          "dbVendor": "dbvoracle",
          "fileNames": [
            "sql.txt"
          ],
          "createTime": "2020-09-08 10:16:11",
          "status": "delete",
          "sessionId": "a9f751281f8ef6936c554432e169359190d392565208931f201523e08036109d_1599531372233"
        }
      }
    ```        
   
* **/sqlflow/job/displayUserJobGraph** 
  * Description: get the sqlflow job's model and graph
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true
    * **jobId**: job id, the value is from user jobs summary detail, required **true**
    * database: selected database, required false
    * schema: selected schema, required false
    * table: selected table, required false
    * isReturnModel: whether return the sqlflow model, required false, default value is true
    * showRelationType: show relation type, required false, default value is **fdd**, multiple values seperated by comma like fdd,frd,fdr. Available values:
      * **fdd**: value of target column from source column
      * **frd**: the recordset count of target column which is affect by value of source column
      * **fdr**: value of target column which is affected by the recordset count of source column
      * **join**: combine rows from two or more tables, based on a related column between them
    * simpleOutput: whether output relation simply, required false, default value is false
    * ignoreRecordSet: whether ignore the record sets, required false, default value is false  
    * showLinkOnly: whether show relation linked columns only, required false, default value is true 
    * hideColumn: whether hide the column ui, required false, default value is false 
    * ignoreFunction: whether ignore the function relations, required false, default value is false 
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.   
  * Sample:
    * test sql file: D:\sql.txt
    * job id: bb996c1ee5b741c5b4ff6c2c66c371dd
    * curl command: 
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/job/displayUserJobGraph?showRelationType=fdd&showRelationType=" -H "accept:application/json;charset=utf-8" -F "userId=google-oauth2|104002923119102769706" -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE" -F "jobId=bb996c1ee5b741c5b4ff6c2c66c371dd" -F "ignoreFunction=true" -F "ignoreRecordSet=true" -F "isReturnModel=false" -F "jobId=bb996c1ee5b741c5b4ff6c2c66c371dd" -F "table=user"
    ```
    * response: 
    ```json    
     {
       "code": 200,
       "data": {
         "mode": "global",
         "summary": {
           ...
         },
         "graph": {
           "elements": {
             "tables": [
               ...
             ],
             "edges": [
               ...
             ],               
           },
           "tooltip": {},
           "relationIdMap": {
             ...
           },
           "listIdMap": {
             ...
           }
         }
       },
       "sessionId": "a9f751281f8ef6936c554432e169359190d392565208931f201523e08036109d_1599531372233"
     }
    ```
    
* **/sqlflow/job/updateUserJobGraphCache**
  * Description: update the user job graph cache, then user can call **/sqlflow/generation/sqlflow/selectedgraph** by sessionId, the sessionId value is from job detail.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **token**: the token of sqlflow client request. sqlflow web, required false, sqlflow client, required true
    * **jobId**: job id, the value is from user job detail, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.            
  * Sample:
    * test sql file: D:\sql.txt
    * job id: bb996c1ee5b741c5b4ff6c2c66c371dd
    * curl command: 
    ```bash
      curl -X POST "http://127.0.0.1:8081/gspLive_backend/sqlflow/job/updateUserJobGraphCache" -H "Request-Origion:SwaggerBootstrapUi" -H "accept:application/json;charset=utf-8"  -F "userId=google-oauth2|104002923119102769706" -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE"  -F "jobId=bb996c1ee5b741c5b4ff6c2c66c371dd"
    ```
    * response: 
    ```json
      {
        "code": 200,
        "data": {
          "sessionId": "a9f751281f8ef6936c554432e169359190d392565208931f201523e08036109d_1599531372233"
        }
      }
    ```      
## Swagger 
More information, please check the test environment swagger document:

  * http://111.229.12.71:8081/gspLive_backend/doc.html?lang=en
  * Token: `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYwMzc1NjgwMCwiaWF0IjoxNTcyMjIwODAwfQ.EhlnJO7oqAHdr0_bunhtrN-TgaGbARKvTh2URTxu9iU`
