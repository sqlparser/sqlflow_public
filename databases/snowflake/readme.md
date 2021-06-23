# Snowflake column-level data lineage

Discover and visualization lineage from Snowflake database and script.

## Extract DDL from the database

1、database:
```
show databases;
```

2、table, view：
```
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
```
SHOW VIEWS IN %s.%s;
SELECT GET_DDL('VIEW', '%s.%s.%s');
```
4、source code of the procedure
```
SHOW PROCEDURES IN %s.%s;
SELECT GET_DDL('PROCEDURE', '%s.%s.%s');
```

5、source code of the function:
```
SHOW FUNCTIONS IN %s.%s;
SELECT GET_DDL('FUNCTION', '%s.%s.%s');
```

##  a minimum list of permissions need to extract all DDL
`SQLFLOW` in the following script is the role you created and used when
grabit connect to the Snowflake database.

```
 grant select on VIEW information_schema.DATABASES  to role SQLFLOW;
 grant select on VIEW information_schema.TABLES  to role SQLFLOW;
 grant select on VIEW information_schema.COLUMNS  to role SQLFLOW;
 grant all privileges on FUNCTION information_schema.GET_DDL() to role SQLFLOW;

```


## Using the grabit tool
1. [GUI Mode](grabit-snowflake-gui.md)
2. [Command Line](grabit-snowflake-command-line.md)

### Parameters used in grabit tool

#### enableQueryHistory

Fetch SQL queries from the query history if set to `true` default is false.

#### Extract from the query history
This is the SQL query used to get query from the snowflake query history.
```
SELECT
 * 
FROM
 TABLE ( information_schema.query_history ( dateadd ( 'mins',-%s, CURRENT_TIMESTAMP ( ) ), CURRENT_TIMESTAMP ( ) ) ) 
ORDER BY
 start_time;
```

#### permission needs to extract queries from query history
Switch to any database that has the `INFORMATION_SCHEMA` schema.
```
USE DATABASE %s;
```


#### queryHistoryBlockOfTimeInMinutes

When `enableQueryHistory:true`, the interval at which the SQL query was extracted in the query History,default is `30` minutes.

#### queryHistorySqlType
You can specify what's kind of SQL statements need to be sent to the SQLFlow for furhter processing after fetch the queries
from the Snowflake query history.

1. grabit will fetch all queries in the Snowflake query history.
2. if `queryHistorySqlType` is specified, grabit will only pickup those SQL statements
and send it to the SQLFlow for furhter processing. This parameter can be useful if you want to discover
lineage from a specific type of SQL statements.
3. if `queryHistorySqlType` is empty, all queries fetched from the query history will be sent to the SQLFlow server.


Value of `queryHistorySqlType` can be a list of SQL statement types separated by the comma like this: `SELECT,UPDATE,MERGE`.

Here is the list of available values that can be used: **SHOW,SELECT,INSERT,UPDATE,DELETE,MERGE,CREATE TABLE, CREATE VIEW, CREATE PROCEDURE, CREATE FUNCTION**.


for example:

````json
queryHistorySqlType: "SELECT,DELETE"
````

#### snowflakeDefaultRole

This value represents the role of the snowflake database.



