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

Example in `Curl`
```
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/job/submitUserJob" -H "accept:application/json;charset=utf-8" -H "Content-Type:multipart/form-data" -F "userId=YOUR USER ID HERE" -F "token=YOUR TOKEN HERE" -F "sqlfiles=@FIRST FILE PATH" -F "sqlfiles=@SECOND FILE PATH" -F "dbvendor=dbvmssql" -F "jobName=job1"
```

**Note:**
 * **-H "Content-Type:multipart/form-data"** is required
 * Add **@** before the file path
 
Return data: 
```json
{
	"code":200,
	"data":{
		"jobId":"c359aef4bd9641d697732422debd8055",
		"jobName":"job1",
		"userId":"google-oauth2|104002923119102769706",
		"dbVendor":"dbvmssql",
		"dataSource":{
			
		},
		"fileNames":["1.sql","1.zip"],
		"createTime":"2020-12-15 15:14:39",
		"status":"create"
	}
}
```

Please records the jobId field.

### 2. Get job status

 * Get the specify user job status and summary
  
  ```
  /gspLive_backend/sqlflow/job/displayUserJobSummary
  ```
  
  Example in `Curl`
  
  ```json
  curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/job/displayUserJobSummary" -F "jobId=c359aef4bd9641d697732422debd8055" -F "userId=YOUR USER ID HERE" -F "token=YOUR TOKEN HERE"
  ```
  
  Return data:
  ```json
  {
	"code":200,
	"data":{
		"jobId":"c359aef4bd9641d697732422debd8055",
		"jobName":"job1",
		"userId":"google-oauth2|104002923119102769706",
		"dbVendor":"dbvmssql",
		"dataSource":{
			
		},
		"fileNames":["1.sql","1.zip"],
		"createTime":"2020-12-15 15:14:39",
		"status":"success",
		"sessionId":"fe5898d4e1b1a7782352b50a8203ca24c04f5513446e9fb059fc4d584fab4dbf_1608045280033"
	}
  }
  ```
  
 * Get all jobs (include history jobs) status and summary
 
  ```
  /gspLive_backend/sqlflow/job/displayUserJobsSummary
  ```
 
  Example in `Curl`
  
  ```json
  curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/job/displayUserJobsSummary" -F "userId=YOUR USER ID HERE" -F "token=YOUR TOKEN HERE"
  ```
  
 

### 3. Export data lineage
 
 When the job status is **success**, you can export the data lineage in json, csv, graphml formats

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
