# Grabit Using Document

## What is a grabit
Grabit is a supporting tool for SQLFlow, which collects SQL scripts from various data sources for SQLFlow, and then uploading them to SQLFlow for data lineage analysis of these SQL scripts. The analysis results can be viewed in the Web front end of SQLFlow. Meanwhile, the analysis results can also be exported from SQLFlow to local area through Grabit, and the JSON results can be uploaded to Neo4j database.

## How to use Grabit

### Prerequisites
- Java 8 or higher version

setup the PATH like this: (Please change the JAVA_HOME according to your own environment)
```
export JAVA_HOME=/usr/lib/jvm/default-java

export PATH=$JAVA_HOME/bin:$PATH
```

### Configuration
Modify the configure file to set all the setting value 
correctly according to your own environment.

#### SQLFlow Server
This is the SQLFlow server that the grabit send the SQL script to.


- server
Usually, it is the IP address of [the SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/) 
installed on your owner server such as `127.0.0.1` or `http://127.0.0.1`

You may set the value to `https://api.gudusoft.com` if you like to send your SQL script to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com) to get the data lineage result.


- serverPort
Default value is `8081` if you connect to your SQLFlow on-premise server.

However, if you use setup the nginx reverse proxy in the nginx configuration file like this:
```
	location /api/ {
		proxy_pass http://127.0.0.1:8081/;
		proxy_connect_timeout 600s ;
		proxy_read_timeout 600s;
		proxy_send_timeout 600s;
		
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header User-Agent $http_user_agent;  
	}
```
Then, just keep the value of `serverPort` empty and set `server` to the value like this: `http://127.0.0.1/api`.

>Please just leave this value empty if you connect to the SQLFlow Cloud Server by specifing the `https://api.gudusoft.com` 
in the `server`.

- userId
This is the user id that used to connect to the SQLFlow server.
Always set this value to `gudu|0123456789` if you are using the SQLFlow on-premise version.

If you want to connect to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com), you may [request a 30 days premium account](https://www.gudusoft.com/request-a-premium-account/) to 
get the necessary userId and secret code.


Example for on-premise version:
```json
	"SQLFlowServer":{
		"server":"127.0.0.1",
		"serverPort":"8081",
		"userId":"gudu|0123456789",
		"userSecret":"" 
	}
```	

Example for Cloud version:
```json
	"SQLFlowServer":{
		"server":"https://api.gudusoft.com",
		"serverPort":"",
		"userId":"your own user id here",
		"userSecret":"your own secret key here" 
	}
```	


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
