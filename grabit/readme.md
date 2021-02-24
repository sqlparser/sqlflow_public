# Grabit Using Document

## What is a grabit
Grabit is a supporting tool for SQLFlow, which collects SQL scripts from various data sources for SQLFlow, and then uploading them to SQLFlow for data lineage analysis of these SQL scripts. The analysis results can be viewed in the Web front end of SQLFlow. Meanwhile, the analysis results can also be exported from SQLFlow to local area through Grabit, and the JSON results can be uploaded to Neo4j database.

## How to use Grabit

### Prerequisites
- Java 8 or higher version must be installed and configured correctly.

setup the PATH like this: (Please change the JAVA_HOME according to your own environment)
```
export JAVA_HOME=/usr/lib/jvm/default-java

export PATH=$JAVA_HOME/bin:$PATH
```

### Configuration
Modify the configure file to set all parameters correctly according to your own environment.

#### 1. SQLFlow Server
This is the SQLFlow server that the grabit send the SQL script to.

- **server**

Usually, it is the IP address of [the SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/) 
installed on your owner server such as `127.0.0.1` or `http://127.0.0.1`

You may set the value to `https://api.gudusoft.com` if you like to send your SQL script to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com) to get the data lineage result.


- **serverPort**

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

>Please just keep this value empty if you connect to the SQLFlow Cloud Server by specifing the `https://api.gudusoft.com` 
in the `server`.

- **userId, userSecret**

This is the user id that used to connect to the SQLFlow server.
Always set this value to `gudu|0123456789` and keep `userSecret` empty if you are using the SQLFlow on-premise version.

If you want to connect to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com), you may [request a 30 days premium account](https://www.gudusoft.com/request-a-premium-account/) to 
[get the necessary userId and secret code](/sqlflow-userid-secret.md).


Example configuration for on-premise version:
```json
	"SQLFlowServer":{
		"server":"127.0.0.1",
		"serverPort":"8081",
		"userId":"gudu|0123456789",
		"userSecret":"" 
	}
```	

Example configuration for Cloud version:
```json
	"SQLFlowServer":{
		"server":"https://api.gudusoft.com",
		"serverPort":"",
		"userId":"your own user id here",
		"userSecret":"your own secret key here" 
	}
```	

#### 2. optionType
You may collect SQL script from various source such as database, github repo, file system.
This parameter tells grabit where the SQL scripts comes from.

Avaiable values for this parameter:
- 1: database 
- 2: github 
- 3: bitbucket 
- 4: single file 
- 5: Multiple SQL Files Under A Directory

This configuration means the SQL script is collected from a database.
```json
"optionType":1
```	

#### 3. resultType
When you submit SQL script to the SQLFlow server, A job is created on the SQLFlow server
and you can always see the graphic data lineage result in the frontend of the SQLFlow 
by using the browser.

Even better, grabit will fetch the data lineage back to the directory where the grabit is running.
This parameter specify which kind of format is used to store the data lineage result.

Avaiable values for this parameter:
- 1: json, data lineage result in json.
- 2: csv, data lineage result in CSV format.
- 3: diagram, in graphml format that can be viewed by yEd.
	
This sample configuration means the output format is json
```json
"resultType":1
```	
	
#### 4. databaseType
This parameter specify the database dialect of the SQL scripts that been analyzed by the SQLFlow.

```txt
	access,bigquery,couchbase,dax,db2,greenplum,hana,hive,impala,informix,mdx,mssql,
	sqlserver,mysql,netezza,odbc,openedge,oracle,postgresql,postgres,redshift,snowflake,
	sybase,teradata,soql,vertica
```
	
This sample configuration means the SQL dialect is SQL Server database.
```json
"databaseType":"sqlserver"
```	
	
#### 5. databaseServer
Specify a database instance that grabit will connect to fetch the metadata that helps SQLFlow 
make a more precise analysis and get a more accurate result of data lineage. 

This parameter must be specified if you set `optionType=1` which means the source of SQL script
comes from a database. Otherwise, it can be leave empty.

- **hostname**

The IP of the datbase server that connect to.

- **port**

The port number of the datbase server that connect to.

- **username**

The database user used to login to the database.

- **password**

The password of the database user.

- **sid**

Name of the Oracle instance. Used for Oracle only.

- **extractedSchemas**
This option is used for Oracle only. 

Comma separated list of schemas to extract, or blank to extract all schemas.
`Schema1,Schema2,Schema3`

- **excludedSchemas**
This option is used for Oracle only. 

Comma separated list of schemas to exclude from processing.
If left blank, no schemas will be excluded.
`Schema1,Schema2`

- **extractedDbsSchemas**

List of databases and schemas to extract, separated by
commas, which are to be provided in the format database/schema;
, or blank to extract all databases.
`database1/schema1,database2/schema2,database3`


- **excludedDbsSchemas**

List of databases and schemas to exclude from extraction,
separated by commas
`database1/schema1,database2`

- **enableQueryHistory**

Fetch SQL queries from the query history if set to `true`, default is false.

- **queryHistoryBlockOfTimeInMinutes**

Time interval to extract SQL query from query history if `enableQueryHistory=true`, 
default is `30` minutes.


Sample configuration of a SQL Server database:
```
"hostname":"127.0.0.1",
"port":"1433",
"username":"sa",
"password":"PASSWORD",
"sid":"",
"extractSchema":"AdventureWorksDW2019/dbo",
"excludedSchema":"",
"enableQueryHistory":false,
"queryHistoryBlockOfTimeInMinutes":30
```


#### 6. SQLInSingleFile
When `optionType=4`, this is a single SQL file need to be analyzed. 

- **filePath**

The name of the SQL file with full path.

#### 7. SQLInDirectory
When `optionType=5`, SQL files under this directory including sub-directory will be analyzed. 

- **filePath**

The directory which includes the SQL files.

#### 8. githubRepo, bitbucketRepo
When `optionType=2`, grabit will fetch SQL files from a specified github repo,
When `optionType=3`, grabit will fetch SQL files from a specified bitbucket repo 

Both sshkey and account password authentication methods are supported.

- **url**

GitHub or BitBucket reop url
	
- **username**

- **password**

- **sshkeyPath**

ssh key file path



	
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
    "isUploadNeo4j":0
}
````

**Configuration file template details explain:** 
````




githubRepo&bitbucketRepo: connection information for operation type GitHub or BitBucket


SQLInSingleFile: path to a file with operation type Single File

SQLInDirectory: path to a file with operation type Multiple SQL Files Under A Directory

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
