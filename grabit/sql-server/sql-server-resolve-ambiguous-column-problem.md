### 2. Discover data lineage in a SQL script file with the metadata from the SQL Server database

Let's say we like to get data linage from this sample SQL:

```SQL
SELECT e.firstName, e.SalesTerritoryKey, SalesTerritoryRegion
FROM dbo.DimEmployee e
left join dbo.DimSalesTerritory d
on e.SalesTerritoryKey = d.SalesTerritoryKey
```

With this configuration:
```json
{
	"optionType":4,
	"resultType":1,
	"databaseType":"sqlserver",
	"SQLFlowServer":{
		"server":"http://111.229.12.71",
		"serverPort":"8081",
		"userId":"gudu|0123456789",
		"userSecret":"" 
	},	
	"SQLInSingleFile":{
	    "filePath":"/home/ubuntu/grabit-2.4.8/sample/demo.sql"
	},
	"enableGetMetadataInJSONFromDatabase":0
}
```

![data lineage without metadata](./sql-server-data-lineage-without-metadata.png "data lineage without metadata")

As you can see, due to the lack of metadata information, 
column `SalesTerritoryRegion` is linked to table: `dbo.DimEmployee`, which is not correct.

We can fetch metadata from the SQL server by specifing `enableGetMetadataInJSONFromDatabase=1`
and `databaseServer` like this:

```json
{
	"optionType":4,
	"resultType":1,
	"databaseType":"sqlserver",
	"SQLFlowServer":{
		"server":"http://111.229.12.71",
		"serverPort":"8081",
		"userId":"gudu|0123456789",
		"userSecret":"" 
	},	
	"SQLInSingleFile":{
	    "filePath":"/home/ubuntu/grabit-2.4.8/sample/demo.sql"
	},
	"enableGetMetadataInJSONFromDatabase":1,
	"databaseServer":{
		"hostname":"115.159.225.38",
		"port":"1433",
		"username":"sa",
		"password":"Sql_flow@77777777",
		"sid":"",
		"extractSchema":"",
		"excludedSchema":"",
		"extractedDbsSchemas":"AdventureWorksDW2019",
        "excludedDbsSchemas":"",
		"enableQueryHistory":false,
		"queryHistoryBlockOfTimeInMinutes":30
	}
}
```

Now, you can get the full data lineage correctly without any ambiguous
![data lineage with metadata](sql-server-data-lineage-with-metadata.png "data lineage with metadata")

