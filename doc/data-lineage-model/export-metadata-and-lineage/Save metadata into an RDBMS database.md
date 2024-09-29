There are 2 tables created in the database in order to store the metadata.

### sqlflow_dbobjects

This table is used to store metadata of all database objects except column which is stored in `sqlflow_columns` table.

#### fields

1. guid, this is the unique identity number of the object
2. parent_id, the guid of the parent object.
3. qualified_name, the fully qualified object name
4. object_type,  type of this object.
5. ddl, the SQL script used to define this object, such as create table statement.
6. ddl_hashId, hash code of the ddl to unique identify a ddl
7. comment, comment about this object

qualified_name should be unique in the same object_type.

So, there is a unique key of this table: (qualified_name, object_type).

Available value for object_type is: cluster, database, table, view, column, procedure, function, trigger.

The following predefined rows should be insert into this table:

```sql
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('101','1','sqldialect','bigquery');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('102','1','sqldialect','couchbase');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('103','1','sqldialect','dax');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('104','1','sqldialect','db2');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('105','1','sqldialect','exasol');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('106','1','sqldialect','greenplum');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('107','1','sqldialect','hana');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('108','1','sqldialect','hive');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('109','1','sqldialect','impala'); 
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('121','1','sqldialect','informix');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('122','1','sqldialect','mdx');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('123','1','sqldialect','mysql');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('124','1','sqldialect','netezza');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('125','1','sqldialect','odbc');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('126','1','sqldialect','openedge');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('127','1','sqldialect','oracle');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('128','1','sqldialect','postgresql');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('129','1','sqldialect','redshift');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('121','1','sqldialect','snowflake'); 
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('122','1','sqldialect','sparksql');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('123','1','sqldialect','sqlserver'); 
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('124','1','sqldialect','sybase');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('125','1','sqldialect','teradata');
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('126','1','sqldialect','vertica');
```

#### insert a new cluster

insert a new hive cluster, with name `primary` and link to `hive` sql dialect which id is `108`

```sql
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('1001','108','cluster','primary');
```

#### insert a new database

```sql
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('2001','1001','database','sampledb@primary');
```

### insert a new table

```sql
insert into sqlflow_dbobjects(guid,parent_id,object_type,qualified_name) values ('3001','2001','table','sampledb.tableA@primary');
```

### sqlflow_columns

This table is used to store all columns.

#### fields

1. guid, this is the unique identity number of the column
2. parent_id, the guid of the table which includes this column
3. qualified_name, the fully qualified object name
4. comment, comment about this column

#### insert a column

```sql
insert into sqlflow_dbobjects(guid,parent_id,qualified_name,comment) 
values ('3001','2001','sampledb.tableA.columnB@primary','this is the comment');
```
