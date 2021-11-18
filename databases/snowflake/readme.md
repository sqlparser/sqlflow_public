# Snowflake column-level data lineage

Discover and visualization lineage from Snowflake database and script.

## Extract DDL from the database

1、database:
```sql
show databases;
```

2、table, view：
```sql
select
  '"' || t.table_catalog || '"' as dbName,
  '"' || t.table_schema || '"' as schemaName,
  '"' || t.table_name || '"' as tableName,
  case when t.table_type = 'VIEW' then 'true'
       when t.table_type = 'BASE TABLE' then 'false'
       else 'false'
  end as isView,
  '"' || c.column_name || '"' as columnName,
  c.data_type,
  null as comments
from
  "%s".information_schema.tables t,
  "%s".information_schema.columns c
where
  t.table_catalog = c.table_catalog
  and t.table_schema = c.table_schema
  and t.table_name = c.table_name
  and upper(t.table_schema) not in ('INFORMATION_SCHEMA')
order by t.table_catalog, t.table_schema, t.table_name, c.ordinal_position;
```
3、source code of the view
```sql
SHOW VIEWS IN %s.%s;
SELECT GET_DDL('VIEW', '%s.%s.%s');
```
4、source code of the procedure
```sql
SHOW PROCEDURES IN %s.%s;
SELECT GET_DDL('PROCEDURE', '%s.%s.%s');
```

5、source code of the function:
```sql
SHOW FUNCTIONS IN %s.%s;
SELECT GET_DDL('FUNCTION', '%s.%s.%s');
```

##  a minimum list of permissions need to extract all DDL
`SQLFLOW` in the following script is the role you created and used when
grabit connect to the Snowflake database.

Or, the user connect to the Snowflake with the role has the following privileges.
```sql
 grant select on VIEW information_schema.DATABASES  to role SQLFLOW;
 grant select on VIEW information_schema.TABLES  to role SQLFLOW;
 grant select on VIEW information_schema.COLUMNS  to role SQLFLOW;
 grant all privileges on FUNCTION information_schema.GET_DDL() to role SQLFLOW;
```


## Using the grabit tool
1. [GUI Mode](grabit-snowflake-gui.md)
2. [Command Line](grabit-snowflake-command-line.md)

### Parameters used in grabit tool

####  hostname

The IP of the database server that the grabit connects.

#### port

The port number of the database server that the grabit connect.

#### username

The database user used to login to the database.

#### password

The password of the database user.

note: the passwords can be encrypted using tools [Encrypted password](#Encrypted password), using encrypted passwords more secure.

#### privateKeyFile

Use a private key to connect.

#### privateKeyFilePwd

Generate the password for the private key.

#### database

The name of the database instance to which it is connected, it is optional.

#### extractedDbsSchemas

List of databases and schemas to extract, separated by
commas, which are to be provided in the format database/schema;
Or blank to extract all databases.
`database1/schema1,database2/schema2,database3` or `database1.schema1,database2.schema2,database3`
When parameter `database` is filled in, this parameter is considered a schema.
And support wildcard characters such as `database1/*`,`*/schema`,`*/*`.

for example:
````json
extractedDbsSchemas: "MY/ADMIN"
````


#### excludedDbsSchemas

This parameters works under the resultset filtered by `extractedDbsSchemas`.
List of databases and schemas to exclude from extraction, separated by commas
`database1/schema1,database2` or `database1.schema1,database2` 
When parameter `database` is filled in, this parameter is considered a schema.
And support wildcard characters such as `database1/*`,`*/schema`,`*/*`.

for example:
````json
excludedDbsSchemas: "MY/*"
````

#### extractedStoredProcedures

A list of stored procedures under the specified database and schema to extract, separated by
commas, which are to be provided in the format database.schema.procedureName or schema.procedureName;
Or blank to extract all databases, support expression.
`database1.schema1.procedureName1,database2.schema2.procedureName2,database3.schema3,database4` or `database1/schema1/procedureName1,database2/schema2`

for example:

````json
extractedStoredProcedures: "database.scott.vEmp*"
````

or

````json
extractedStoredProcedures: "database.scott"
````

#### extractedViews

A list of stored views under the specified database and schema to extract, separated by
commas, which are to be provided in the format database.schema.viewName or schema.viewName.
Or blank to extract all databases, support expression.
`database1.schema1.procedureName1,database2.schema2.procedureName2,database3.schema3,database4` or `database1/schema1/procedureName1,database2/schema2`

for example:

````json
extractedViews: "database.scott.vEmp*"
````

or

````json
extractedViews: "database.scott"
````

#### enableQueryHistory

Fetch SQL queries from the query history if set to `true` default is false.

#### Extract from the query history
This is the SQL query used to get query from the snowflake query history,We can extract data from the last year.
```sql
SELECT
*
FROM
"SNOWFLAKE"."ACCOUNT_USAGE"."QUERY_HISTORY"
WHERE
dateadd('mins',
-%s,
current_timestamp()) <= start_time ORDER BY start_time;

```

#### permission needs to extract queries from query history

You must define a role that has access to the `SNOWFLAKE` database,And assign `WAREHOUSE` permission to this role.

Assign permissions to a role, for example:

````sql
#create role
use role accountadmin;
grant imported privileges on database snowflake to role sysadmin;
grant imported privileges on database snowflake to role customrole1;
use role customrole1;
select * from snowflake.account_usage.databases;

#To do this, the Role gives the WAREHOUSE permission
select current_warehouse()
use role sysadmin
GRANT ALL PRIVILEGES ON WAREHOUSE %current_warehouse% TO ROLE customrole1;
````

#### queryHistoryBlockOfTimeInMinutes

When `enableQueryHistory:true`, the interval at which the SQL query was extracted in the query History,default is `30` minutes.

#### queryHistorySqlType

When `enableQueryHistory:true`, the DML type of SQL is extracted from the query History.
When empty, all types are extracted, and when multiple types are specified, a comma separates them, such as `SELECT,UPDATE,MERGE`.
Currently only the snowflake database supports this parameter,support types are **SHOW,SELECT,INSERT,UPDATE,DELETE,MERGE,CREATE TABLE, CREATE VIEW, CREATE PROCEDURE, CREATE FUNCTION**.

for example:

````json
queryHistorySqlType: "SELECT,DELETE"
````

#### snowflakeDefaultRole

This value represents the role of the snowflake database.

####  sqlsourceTableName

table name: **query_table**

| query_name | query_source                        |
| ---------- | ----------------------------------- |
| query1     | create view v1 as select f1 from t1 |
| query2     | create view v2 as select f2 from t2 |
| query3     | create view v3 as select f3 from t3 |

If you save SQL queries in a specific table, one SQL query per row. 

Let's say: `query_table.query_source` store the source code of the query.
We can use this query to fetch all SQL queries in this table:

```sql
select query_name as queryName, query_source as querySource from query_table
```

By setting the value of `sqlsourceTableName` and `sqlsourceColumnQuerySource`,`sqlsourceColumnQueryName`
grabit can fetch all SQL queries in this table and send it to the SQLFlow to analzye the lineage.

In this example, 
```json
"sqlsourceTableName":"query_table"
"sqlsourceColumnQuerySource":"query_source"
"sqlsourceColumnQueryName":"query_name"
```

Please leave `sqlsource_table_name`  empty if you don't fetch SQL queries from a specific table.
 
####  sqlsourceColumnQuerySource
In the above sample:
```json
"sqlsourceColumnQuerySource":"query_source"
```

#### sqlsourceColumnQueryName
```json
"sqlsourceColumnQueryName":"query_name"
```
This parameter is optional, you don't need to speicify a query name column if it doesn't exist in the table.


**eg configuration file:**
````json
{
    "databaseServer":{
        "hostname":"127.0.0.1",
        "port":"433",
        "username":"USERNAME",
        "password":"PASSWORD",
        "privateKeyFile":"",
        "privateKeyFilePwd":"",
        "database":"",
        "extractedDbsSchemas":"MY/dbo",
        "excludedDbsSchemas":"",
        "extractedStoredProcedures":"",
        "extractedViews":"",
        "enableQueryHistory":true,
        "queryHistoryBlockOfTimeInMinutes":30,
        "snowflakeDefaultRole":"",
        "queryHistorySqlType":"",
        "sqlsourceTableName":"",
        "sqlsourceColumnQuerySource":"",
        "sqlsourceColumnQueryName":""
    },
    "SQLFlowServer":{
        "server":"http:127.0.0.1",
        "serverPort":"8081",
        "userId":"gudu|0123456789",
        "userSecret":""
    },
    "SQLScriptSource":"database",
    "lineageReturnFormat":"json",
    "databaseType":"snowflake"
}
````
