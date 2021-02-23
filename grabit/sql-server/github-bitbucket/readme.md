# Grabit Using Document

## Data source type is github or bitbucket
### Step 1: Install git
- **ubuntu:** 
````
sudo apt-get install git
````
- **centos:** 
````
sudo yum install git
````
- **mac:** 
````
brew install git
````
- **windows:** 
````
1.Go to the Git official website to download, website address: https://git-scm.com/downloads
2.Run the Git installation file and click Next to finish the installation
````
After the installation is complete, you can verify that the installation is complete with **git --version** and that the installation was successful if the Git version is displayed.

- **Generate the ssh public and private key**：
````
ssh-keygen -o
````
### Step 2: Install grabit
````
unzip grabit-x.x.x.zip

cd grabit-x.x.x
````
- **linux & mac open permissions** 
````
chmod 777 *.sh
````
After the installation is complete, you can execute the command **./start.sh /f conf-temp** or **./start.bat /f conf-temp**. If the logs directory appears and the **start grabit command** is printed in the log file, the installation is successful.

### Step 3: Set up configuration file

- **1. set up optionType**

You may collect SQL script from various source such as database, github repo, file system. This parameter tells grabit where the SQL scripts comes from.

Avaiable values for this parameter:
````
2: github
3: bitbucket
````

- **2. set up databaseType**

the database type of all connections, the types currently supported：
````
access,bigquery,couchbase,dax,db2,greenplum,hana,hive,impala,informix,mdx,mssql,sqlserver,mysql,netezza,
odbc,openedge,oracle,postgresql,postgres,redshift,snowflake,sybase,teradata,soql,vertica
````

- **3. set up resultType**

output result type.

Avaiable values for this parameter:
````
1: json
2: csv
3: diagram
````

- **4. set up isUploadNeo4j**

whether to upload to neo4j.

Avaiable values for this parameter:
````
1: yes
0: no
````

If the value is 0, no setting is required. If the value is 1, it needs to be set up neo4j connection information, example:
````
"neo4jConnection":{
    "url":"127.0.0.1:7687",
    "username":"neo4j",
    "password":"neo4j"
}
````

- **5. set up githubRepo or bitbucketRepo**

connection information for operation type GitHub or BitBucket.

Parameters to set:
````
url: GitHub or BitBucket reop url
username: account
password: password
sshkeyPath: ssh key file path,sshkey and account password two authentication methods can be filled in either
````

If it's a public library, you just need to set the URL, you don't need to set the username, password, and sshkeyPath, but if it's a private library, you need to set the username, password, or sshkeyPath and fill in one of them, example:
````
"githubRepo":{
    "url":"https://github.com/sqlparser/snowflake-data-lineage",
    "username":"",
    "password":"",
    "sshkeyPath":""
}
````
or:
````
"githubRepo":{
    "url":"https://github.com/my/test",
    "username":"test",
    "password":"123456",
    "sshkeyPath":""
}
````

- **6. set up SQLFlowServer**

This is the SQLFlow server that the grabit send the SQL script to.

Parameters to set:
````
server: sqlflow server address
serverPort: sqlflow server port
userId: sqlflow user id
userSecret: sqlflow user secret
````

Set the information of SQLFlowServer and fill in the "server". If the "server" is the domain name, you do not need to set the "serverPort". If the "server" is IP, you need to set the "serverPort".
note：1，When sqlflow server is connected to the Cloud SQLFlow（server is https://api.gudusoft.com）, official as the default domain name server, don't need to fill in the port, please login on https://sqlflow.gudusoft.com platform, and then obtain userId in the personal account information, and generate the corresponding userSecret 2，When sqlflow server is connected to a local SQLFlow, the server is local IP, the port is 8081, userId in the backend of sqlflow  backend/conf/gudu_sqlflow.conf anonymous_user_id conf file access, default is gudu | 0123456789, userSecret don't have to fill out and the final data need not be filled in to keep the template as it is, example:
````
"SQLFlowServer":{
    "server":"http:127.0.0.1",
    "serverPort":"8081",
    "userId":"gudu|0123456789",
    "userSecret":""
}
````

**eg configuration file:**
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
        "url":"https://github.com/sqlparser/snowflake-data-lineage",
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
        "server":"http:127.0.0.1",
        "serverPort":"8081",
        "userId":"gudu|0123456789",
        "userSecret":""
    },
    "neo4jConnection":{
        "url":"",
        "username":"",
        "password":""
    },
    "optionType":2,
    "resultType":1,
    "databaseType":"snowflake",
    "isUploadNeo4j":0
}
````

### Step 4: Start grabit
- **linux & mac** 
````
./start.sh /f <path_to_config_file>  

note: 
    path_to_config_file: config file path  

eg: 
    ./start.sh /f config.txt
````
- **windows** 
````
./start.bat /f <path_to_config_file>  

note: 
    path_to_config_file: config file path  

eg: 
    ./start.bat /f config.txt
````
After execution, view the **/logs/log.log** file. If the log prints a **submit job to sqlflow successful**. Then it is proved that the upload to SQLFlow has been successful. Log in the SQLFlow website to view the newly analyzed results. In the **Task List**, you can view the analysis results of the currently submitted tasks.If the download analysis result is set, **export json result successful** will appear in the log.

### Grabit detailed usage documentation
[Grabit-Documentation](https://github.com/sqlparser/sqlflow_public/blob/master/grabit/readme.md)
