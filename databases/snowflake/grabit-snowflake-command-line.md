## Automated data lineage from snowflake (Command Line Mode)
This article introduces how to discover the data lineage from snowflake scripts or the snowflake database and automatically update it. 
So the business users and developers can see the snowflake data lineage graph instantly.

### Software used in this solution
- [SQLFlow Cloud](https://sqlflow.gudusoft.com) Or [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/)
- [Grabit tool](https://www.gudusoft.com/grabit/) for SQLFlow. It's free.


### Install grabit tool
After [download grabit tool](https://www.gudusoft.com/grabit/), please [check this article](https://github.com/sqlparser/sqlflow_public/tree/master/grabit) 
to see how to setup the grabit tool.

### Discover data lineage in a snowflake database
- Modify the `conf-template\snowflake-config-template` to meet your environment.

Here is a sample config file: `snowflake-config` that grabs metadata from the remote snowflake database
and sends the metadata to the SQLFlow Cloud to discover the data lineage.

It would help if you had [a premium account](https://github.com/sqlparser/sqlflow_public/blob/master/sqlflow-userid-secret.md) to access the SQLFlow Cloud.


```json
{
	"databaseType":"snowflake",
	"optionType":1,
	"resultType":1,
	"databaseServer":{
		"hostname":"snowflake ip address",
		"port":"443",
		"username":"snowflake user name",
		"password":"your password here",
		"sid":"",
		"extractSchema":"",
		"excludedSchema":"",
		"extractedDbsSchemas":"DEMO_DB/PUBLIC",
        "excludedDbsSchemas":"*/INFORMAITON_SCHEMA",
        "extractedStoredProcedures":"",
        "extractedViews":"",
		"enableQueryHistory":false,
		"queryHistoryBlockOfTimeInMinutes":30
	},
	"SQLFlowServer":{
		"server":"https://api.gudusoft.com",
		"serverPort":"",
		"userId":"your sqlflow premium account id",
		"userSecret":"your sqlflow premium account secret code"
	},
	"neo4jConnection":{
	    "url":"",
        "username":"",
        "password":""
	},
	"isUploadNeo4j":0
}
```

- Run grabit command-line tool, you may find the grabit.log under the logs directory.
```
./start.sh /f snowflake-config
```

- Check out the diagram via this url: [https://sqlflow.gudusoft.com/#/job/latest](https://sqlflow.gudusoft.com/#/job/latest)

- You may save the data lineage in JSON/CSV/GRAPHML format.

	The file will be saved under `data\datalineage` directory.

- Run the grabit at a scheduled time

	[Please check the instructions here](https://github.com/sqlparser/sqlflow_public/tree/master/grabit#run-the-grabit-at-a-scheduled-time)

