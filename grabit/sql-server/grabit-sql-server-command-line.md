## Automated data lineage from SQL Server (Command Line Mode)
This article introduces how to discover the data lineage from SQL Server scripts or the SQL Server database and automatically update it. 
So the business users and developers can see the SQL Server data lineage graph instantly.

### Software used in this solution
- [SQLFlow Cloud](https://sqlflow.gudusoft.com) Or [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/)
- [Grabit tool](https://www.gudusoft.com/grabit/) for SQLFlow. It's free.


### Install grabit tool
After [download grabit tool](https://www.gudusoft.com/grabit/), please [check this article](https://github.com/sqlparser/sqlflow_public/tree/master/grabit) 
to see how to setup the grabit tool.

### Discover data lineage in a SQL Server database
- Modify the `conf-template\sqlserver-config-template` to meet your environment.

Here is a sample config file: `sqlserver-config` that grabs metadata from a local SQL Server database
and sends the metadata to the SQLFlow Cloud to discover the data lineage.

It would help if you had [a premium account](https://github.com/sqlparser/sqlflow_public/blob/master/sqlflow-userid-secret.md) to access the SQLFlow Cloud.


```json
{
	"databaseServer":{
		"hostname":"sql server ip address",
		"port":"1433",
		"username":"sql server user name",
		"password":"your password here",
		"sid":"",
		"extractSchema":"",
		"excludedSchema":"",
		"extractedDbsSchemas":"",
        "excludedDbsSchemas":"master/dbo,master/sys,master/INFORMAITON_SCHEMA,msdb/dbo,tempdb/dbo,tempdb/sys,model/dbo",
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
	"optionType":1,
	"resultType":1,
	"databaseType":"sqlserver",
	"isUploadNeo4j":0
}
```

- Run grabit command-line tool 
```
./start.sh /f sqlserver-config
```

	You may find the grabit.log under the logs directory.

- Check out the diagram via this url: [https://sqlflow.gudusoft.com/#/job/latest](https://sqlflow.gudusoft.com/#/job/latest)

- You may save the data lineage in JSON/CSV/GRAPHML format.

	The file will be saved under `data\datalineage` directory.

- Run the grabit at a scheduled time

	[Please check the instructions here](https://github.com/sqlparser/sqlflow_public/tree/master/grabit#run-the-grabit-at-a-scheduled-time)

