## connect to hive metastore

Use grabit command line to connect to a MySQL database that save the 
Hive metastore. Fetch the metadata from the Hive metastore and send
to the SQLFlow to analyze the data lineage.

### config file
```json
{
    "databaseServer":{
        "hostname":"",
        "port":"3306",
        "username":"",
        "password":"",
        "database":"",
        "extractedDbsSchemas":"",
        "excludedDbsSchemas":"",
        "extractedStoredProcedures":"",
        "extractedViews":"",
        "metaStore":"hive"
    },
    "SQLFlowServer":{
        "server":"http://127.0.0.1",
        "serverPort":"8081",
        "userId":"gudu|0123456789",
        "userSecret":""
    },
    "SQLScriptSource":"database",
    "lineageReturnFormat":"json",
    "databaseType":"mysql"
}
```

Please make sure to setup the `database` to the name of the MySQL database 
which store the Hive metastore.

The IP below should be the machine where the SQLFlow on-premise version is installed.
```
"server":"http://127.0.0.1",
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
