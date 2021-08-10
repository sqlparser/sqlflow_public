## connect to hive metastore

Use grabit command line to connect to a MySQL database that save the 
Hive metastore. Fetch the metadata from the Hive metastore and send
to the SQLFlow to analyze the data lineage.

### config file
```json
{
    "databaseServer":{
        "hostname":"115.159.225.38",
        "port":"3306",
        "username":"root",
        "password":"123456a?",
        "database":"hive",
        "extractedDbsSchemas":"",
        "excludedDbsSchemas":"",
        "extractedStoredProcedures":"",
        "extractedViews":"",
        "metaStore":"hive"
    },
    "SQLFlowServer":{
        "server":"http:127.0.0.1",
        "serverPort":"8081",
        "userId":"gudu|0123456789",
        "userSecret":""
    },
    "SQLScriptSource":"database",
    "lineageReturnFormat":"json",
    "databaseType":"mysql"
}
```


### command line syntax
- **mac & linux**
```shell script
chmod +x start.sh

sh start.sh /f config.json
```

- **windows**
```bat
start.bat /f config.json
```

## download the latest version grabit tool
https://www.gudusoft.com/grabit/
