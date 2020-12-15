## SQLFlow Job API tutorial

This article describes how to use the Job Rest API provided by the SQLFlow to 
communicate with the SQLFlow server and export the data lineage in json, csv, graphml formats.

### Prerequisites
To use the Rest API of the SQLFlow, you need to <a href="https://gudusoft.com">obtain a premium account</a>. 
After that, you will get the `userid` and `secret key`, which will be used in the API.

- User ID
- Secrete Key

More detail, please see https://github.com/sqlparser/sqlflow_public/edit/master/api/sqlflow_api_tutorial.md

### Call Rest API

#### 1. Submit a sqlflow job

Call this API by sending the SQL files and get the result includes the data lineage. SQLFlow job supports both of multiple files and zip archive file.

```
/gspLive_backend/sqlflow/job/submitUserJob
```

### 2. Get job status

 * Get the specify user job status and summary
  ```
  /gspLive_backend/sqlflow/job/displayUserJobSummary
  ```
  
 * Get all jobs (include history jobs) status and summary
 ```
 /gspLive_backend/sqlflow/job/displayUserJobsSummary
 ```

### 3. Export data lineage

 * Export data lineage in json format
  
  ```
  /gspLive_backend/sqlflow/job/exportLineageAsJson
  ```
 
 * Export data lineage in csv format
  
  ```
  /gspLive_backend/sqlflow/job/exportLineageAsCsv
  ```
 
 * Export data lineage in graphml format, you can view the lineage graph at yEd Graph Editor
   
  ```
  /gspLive_backend/sqlflow/job/exportLineageAsGraphml
  ``` 
