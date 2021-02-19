# grabit-python Using Document
## What is a grabit
Grabit, a Python enabled version of SQLFlow, collects SQL scripts from files or folders and uploads them to SQLFlow for data lineage analysis of these SQL scripts. The analysis results can be viewed in the Web front end of SQLFlow. At the same time, analysis results can also be exported locally from SQLFlow via Grabit.
## How to use Grabit
````
python Grabit.py /s server /p port /u userId /k screctKey /t databaseType /f path_to_config_file /r resultType 

eg: 
    python Grabit.py /u 'auth0|xxx' /k cab9712c45189014a94a8b7aceeef7a3db504be58e18cd3686f3bbefd078ef4d /s https://api.gudusoft.com /t dbvoracle /f /Users/Documents/gsp_sqlfiles-master/TestCases/oracle/delete.sql /r 1
note:
    If the string contains userId "|" pipe such symbols, userId must use single quotes (' ')
````

**Script parameter interpretation:** 
````
path_to_config_file: path to a file with operation type Single File or path to a file with operation type Multiple SQL Files Under A Directory
server: sqlflow server address
port: sqlflow server port
userId: sqlflow user id
screctKey: sqlflow user secret
    note：
        1，When sqlflow server is connected to the Cloud SQLFlow（server is https://sqlflow.gudusoft.com）, official as the default domain name server, 
        don't need to fill in the port, please login on https://sqlflow.gudusoft.com platform, and then obtain userId in the personal account information, 
        and generate the corresponding userSecret
        2，When sqlflow server is connected to a local SQLFlow, the server is local IP, the port is 8081, userId in the backend of sqlflow 
        backend/conf/gudu_sqlflow.conf anonymous_user_id conf file access, default is gudu | 0123456789, userSecret don't have to fill out        

databaseType: the database type of all connections, the types currently supported：
     dbvbigquery, dbvcouchbase,dbvdb2,dbvgreenplum,dbvhana,dbvhive,dbvimpala,
     dbvinformix,dbvmdx,dbvmysql,dbvnetezza,dbvopenedge,dbvoracle,dbvpostgresql,
     dbvredshift,dbvsnowflake,dbvmssql,dbvsybase,dbvteradata,dbvvertica


resultType: output result type (Integer)
    1: json
    2: csv
    3: diagram
````
