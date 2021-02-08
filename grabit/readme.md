# Grabit Using Document

## What is a grabit
Grabit is a supporting tool for SQLFlow, which collects SQL scripts from various data sources for SQLFlow, and then uploading them to SQLFlow for data lineage analysis of these SQL scripts. The analysis results can be viewed in the Web front end of SQLFlow. Meanwhile, the analysis results can also be exported from SQLFlow to local area through Grabit, and the JSON results can be uploaded to Neo4j database.

## How to use Grabit
### grabit ui launch
##### mac & linux
`
./start.sh
`
##### windows
`
start.bat
`
### grabit cmd launch
#### step 1. set config file

**Configuration file template:** 
````
{
    "databaseServer":{
        "hostname":"",
        "port":"",
        "username":"",
        "password":"",
        "sid":"",
        "extractSchema":"",
        "excludedSchema":"",
        "enableQueryHistory":false,
        "queryHistoryBlockOfTimeInMinutes":30
    },
    "githubRepo":{
        "url":"",
        "username":"",
        "password":"",
        "sshkeyPath":""
    },
    "bitbucketRepo":{
        "url":"",
        "username":"",
        "password":"",
        "sshkeyPath":""
    },
    "SQLInSingleFile":{
        "filePath":""
    },
    "SQLInDirectory":{
        "filePath":""
    },
    "SQLFlowServer":{
        "server":"https://api.gudusoft.com",
        "serverPort":"",
        "userId":"gudu|0123456789",
        "userSecret":""
    },
    "neo4jConnection":{
        "url":"",
        "username":"",
        "password":""
    },
    "optionType":1,
    "resultType":1,
    "databaseType":"",
    "isUploadNeo4j":0
}
````

**Configuration file template details explain:** 
````
optionType: data source type (Integer)
    1: database 
    2: github 
    3: bitbucket 
    4: single file 
    5: Multiple SQL Files Under A Directory

databaseServer: the operation type is connection information for the database
    hostname: server host name
    port: port
    username: account
    password: password
    sid: database
    extractSchema: exporting JSON data to extract Schema
    excludedSchema: exporting JSON data to excluded Schema
    enableQueryHistory: whether to enable query history execution SQL (Boolean)
    queryHistoryBlockOfTimeInMinutes: query how long (in minutes) the history of the execution of SQL functionality (Integer)

githubRepo&bitbucketRepo: connection information for operation type GitHub or BitBucket
    url: GitHub or BitBucket reop url
    username: account
    password: password
    sshkeyPath: ssh key file path,sshkey and account password two authentication methods can be filled in either

SQLInSingleFile: path to a file with operation type Single File

SQLInDirectory: path to a file with operation type Multiple SQL Files Under A Directory

SQLFlowServer: connection information to connect to SQLFlow
    server: sqlflow server address
    serverPort: sqlflow server port
    userId: sqlflow user id
    userSecret: sqlflow user secret
    note：
        1，When sqlflow server is connected to the Cloud SQLFlow（server is https://sqlflow.gudusoft.com）, official as the default domain name server, 
        don't need to fill in the port, please login on https://sqlflow.gudusoft.com platform, and then obtain userId in the personal account information, 
        and generate the corresponding userSecret
        2，When sqlflow server is connected to a local SQLFlow, the server is local IP, the port is 8081, userId in the backend of sqlflow 
        backend/conf/gudu_sqlflow.conf anonymous_user_id conf file access, default is gudu | 0123456789, userSecret don't have to fill out        

databaseType: the database type of all connections, the types currently supported：
	access,bigquery,couchbase,dax,db2,greenplum,hana,hive,impala,informix,mdx,mssql,
	sqlserver,mysql,netezza,odbc,openedge,oracle,postgresql,postgres,redshift,snowflake,
	sybase,teradata,soql,vertica

resultType: output result type (Integer)
    1: json
    2: csv
    3: diagram

isUploadNeo4j: whether to upload to neo4j (Integer)
    1: yes
    0: no (default)

neo4jConnection: connection information to connect to neo4j database
    url: neo4j database connection url
    username: account
    password: password
````

#### step 2. Usage
##### mac & linux
````
./start.sh /f <path_to_config_file>  

note: 
    path_to_config_file: config file path  

eg: 
    ./start.sh /f config.txt
````
##### windows
````
./start.bat /f <path_to_config_file>  

note: 
    path_to_config_file: config file path  

eg: 
    start.bat /f config.txt
````
### grabit job 
#### use mac & linux crontab
````
cron ./start_job.sh /f <path_to_config_file> <lib_path>

note: 
    path_to_config_file: config file path 
    lib_path: lib directory absolute path

eg: 
    1. sudo vi /etc/crontab 
    2. add the following statement to the last line
        0 */1   * * * ubuntu /home/ubuntu/grabit-2.4.6/start_job.sh /f /home/ubuntu/grabit-2.4.6/conf-oracle /home/ubuntu/grabit-2.4.6/lib
        
        note: 
            0 */1   * * *: cron expression
            ubuntu: The name of the system user performing the task
            /home/ubuntu/grabit-2.4.6/start_job.sh: The path of the task script
            /f /home/ubuntu/grabit-2.4.6/conf-oracle: config file path
            /home/ubuntu/grabit-2.4.6/lib: lib directory absolute path
    3.sudo service cron restart    
````
