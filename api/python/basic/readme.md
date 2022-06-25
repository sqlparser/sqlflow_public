## Python Data lineage: using the SQLFlow REST API (Basci) 

A basic tutorial for using the Python version of the SQLFlow API.

Here is an advanced version of how to use [Python to get the data lineage](https://github.com/sqlparser/sqlflow_public/tree/master/api/python/advanced).

### Prerequisites

- Python 2.7 or higher version must be installed and configured correctly.

- Installing Dependency Libraries: 

`
pip install requests
`

### GenerateTokenDemo.py

This demo shows how to get a token from a SQLFlow system that can be used to legally call other interfaces.

* Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **userSecret**: the userSecret of sqlflow client request. sqlflow web, required false, sqlflow client, required true

This is the user id that is used to connect to the SQLFlow server.
Always set this value to `gudu|0123456789` and keep `userSecret` empty if you use the SQLFlow on-premise version.

If you want to connect to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com), you may [request a 30 days premium account](https://www.gudusoft.com/request-a-premium-account/) to 
[get the necessary userId and secret code](/sqlflow-userid-secret.md).

**set the parameters in the code**

Connect to the SQLFlow Cloud Server:

````json
    url = 'https://api.gudusoft.com/gspLive_backend/user/generateToken'
    userId = 'YOUR USER ID'
    screctKey = 'YOUR SECRET KEY'
````

Connect to the SQLFlow on-premise version:

````json
    url = 'http://127.0.0.1:8081/gspLive_backend/user/generateToken'
    userId = 'gudu|012345678'
    screctKey = ''
````

**start script**

`python GenerateTokenDemo.py`

### GenerateDataLineageDemo.py

This demo shows how to get the desired SQL script analysis results from the SQLFlow system.

* Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **userSecret**: the userSecret of sqlflow client request. sqlflow web, required false, sqlflow client, required true
    * sqltext: sql text, required false
    * sqlfile: sql file, required false
    * **dbvendor**: database vendor, required **true**, available values: 
      * dbvbigquery, dbvcouchbase,dbvdb2,dbvgreenplum,dbvhana,dbvhive,dbvimpala,dbvinformix,dbvmdx,dbvmysql,dbvnetezza,dbvopenedge,dbvoracle,dbvpostgresql,dbvredshift,dbvsnowflake,dbvmssql,dbvsybase,dbvteradata,dbvvertica
    * filePath: data lineage file path


**set the parameters in the code**

Connect to the SQLFlow Cloud Server:

````json
    tokenUrl = 'https://api.gudusoft.com/gspLive_backend/user/generateToken'
    generateDataLineageUrl = 'https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow'
    userId = 'YOUR USER ID'
    screctKey = 'YOUR SECRET KEY'
    sqlfile = 'test.sql'
    ignoreRecordSet = False
    dbvendor = 'dbvoracle'
    showRelationType = 'fdd'
    simpleOutput = False
````

Connect to the SQLFlow on-premise version:

````json
    tokenUrl = 'http://127.0.0.1:8081/gspLive_backend/user/generateToken'
    generateDataLineageUrl = 'http://127.0.0.1:8081/gspLive_backend/sqlflow/generation/sqlflow'
    userId = 'gudu|012345678'
    screctKey = ''
    sqlfile = 'test.sql'
    ignoreRecordSet = False
    dbvendor = 'dbvoracle'
    showRelationType = 'fdd'
    simpleOutput = False
````

**start script**

cmd:

-  /f. the sqlfile path，required. eg: /f sql.txt
-  /o. the data lineage file type. default value is json, optional. eg: /o csv , /o json

eg:

`python GenerateDataLineageDemo.py /f test.sql /o csv`


