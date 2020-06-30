# SQLFlow WebAPI

## JWT Authorization
* All of the restful requests are based on JWT authorization. Before accessing the sqlflow WebAPI, user needs to obtain the corresponding JWT token for legal access.
* How to use JWT Token for security authentication?
  * In the header of the HTTP request, please pass the parameters:
   ```
     Key:      Authorization
     Value:    Token <token>
  ```

## WebAPI

### Sqlflow Generation Interface  

* **/sqlflow/generation/sqlflow**
  * Description: generate sqlflow model
  * HTTP Method: **POST**
  * Parameters: 
    * sqltext: sql text, required false
    * sqlfile: sql file, required false
    * **dbvendor**: database vendor, required **true**
    * showRelationType: show relation type, required false, default value is fdd
    * simpleOutput: whether simple output relation, required false, default value is false
    * ignoreRecordSet: whether ignore the record set, required false, default value is false
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.  
    
* **/sqlflow/generation/sqlflow/graph**
  * Description: generate sqlflow model and graph
  * HTTP Method: **POST**
  * Parameters: 
    * sqltext: sql text, required false
    * sqlfile: sql file, required false
    * **dbvendor**: database vendor, required **true**
    * showRelationType: show relation type, required false, default value is fdd
    * simpleOutput: whether output relation simply, required false, default value is false
    * ignoreRecordSet: whether ignore the record sets, required false, default value is false  
    * showLinkOnly: whether show relation linked columns only, required false, default value is true 
    * hideColumn: whether hide the column ui, required false, default value is false 
    * ignoreFunction: whether ignore the function relations, required false, default value is false 
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.  
    
* **/sqlflow/generation/sqlflow/selectedgraph**          
  * Description: generate sqlflow model and selected dbobject graph
  * HTTP Method: **GET POST**
  * Parameters: 
    * **sessionId**: request sessionId, the value is from api **/sqlflow/generation/sqlflow/graph**, required **true**
    * database: selected database, required false
    * schema: selected schema, required false
    * table: selected table, required false
    * isReturnModel: whether return the sqlflow model, required false, default value is true
    * **dbvendor**: database vendor, required **true**
    * showRelationType: show relation type, required false, default value is fdd
    * simpleOutput: whether output relation simply, required false, default value is false
    * ignoreRecordSet: whether ignore the record sets, required false, default value is false  
    * showLinkOnly: whether show relation linked columns only, required false, default value is true 
    * hideColumn: whether hide the column ui, required false, default value is false 
    * ignoreFunction: whether ignore the function relations, required false, default value is false 
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.  

### Sqlflow User Job Interface
* **/sqlflow/job/submitUserJob**
  * Description: submit user job for multiple sql files, support zip file.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: request user id, required **true**
    * **jobName**: job name, required **true**
    * **dbvendor**: database vendor, required **true**
    * **sqlfiles**:  request sql files, please use **multiple parts** to submit the sql files, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.  
    
* **/sqlflow/job/deleteUserJob**
  * Description: delete the user job by job id.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: request user id, required **true**
    * **jobId**: job id, the value is from user job detail, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.  
    
* **/sqlflow/job/displayUserJobsSummary**        
  * Description: get the user jobs summary information.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: request user id, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message. 
    
* **/sqlflow/job/displayUserJobSummary**        
  * Description: get the specify user job information.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: request user id, required **true**
    * **jobId**: job id, the value is from user jobs summary detail, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.  
    
* **/sqlflow/job/displayUserJobGraph** 
  * Description: get the sqlflow job's model and graph
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: request user id, required **true**
    * **jobId**: job id, the value is from user jobs summary detail, required **true**
    * database: selected database, required false
    * schema: selected schema, required false
    * table: selected table, required false
    * isReturnModel: whether return the sqlflow model, required false, default value is true
    * showRelationType: show relation type, required false, default value is fdd
    * simpleOutput: whether output relation simply, required false, default value is false
    * ignoreRecordSet: whether ignore the record sets, required false, default value is false  
    * showLinkOnly: whether show relation linked columns only, required false, default value is true 
    * hideColumn: whether hide the column ui, required false, default value is false 
    * ignoreFunction: whether ignore the function relations, required false, default value is false 
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.   
    
* **/sqlflow/job/updateUserJobGraphCache**
  * Description: update the user job graph cache, then user can call **/sqlflow/generation/sqlflow/selectedgraph** by sessionId, the sessionId value is from job detail.
  * HTTP Method: **POST**
  * Parameters: 
    * **userId**: request user id, required **true**
    * **jobId**: job id, the value is from user job detail, required **true**
  * Return code:
    * 200: successful
    * other: failed, check the error field to get error message.            
    
## Swagger 
More information, please check the test environment swagger document:

http://111.229.12.71:8081/gspLive_backend/swagger-ui.html#
