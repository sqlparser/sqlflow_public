## SQLFlow - A Tool that tracks column-level data lineage

Track Column-Level Data Lineage for more than 20 major databases incluing 
Snowflake, Hive, SparkSQL, Teradata, Oracle, SQL Server, AWS redshift, BigQuery and etc.

Build and visualization lineage from SQL script from query histroy, ETL script,
Github/Bitbucket, Local filesystem and remote databases.

Exploring lineage using interactive diagram or programmatically using Restful APIs or SDKs.

Discover data lineage in this query:
```sql
insert into emp (id,first_name,last_name,city,postal_code,ph)
  select a.id,a.first_name,a.last_name,a.city,a.postal_code,b.ph
  from emp_addr a
  inner join emp_ph b on a.id = b.id;
```

SQLFlow presents a nice clean graph to you that tells
where the data came from, what transformations it underwent along the way, 
and what other data items are derived from this data value.

[![SQLFlow Introduce](images/sqlflow_introduce1.png)](https://sqlflow.gudusoft.com)

### What SQLFlow can do for you
- Provide a nice cleam diagram to the end-user to understand the data lineage quickly.
- Incorporate the lineage metadata decoded from the complex SQL script into your own metadata database for further processing.
- Visualize the metadata already existing in your database to release the power of data.
- Perform impact analysis and root-cause analysis by tracing lineage backwards or forwards with several mouse click.
- Able to process SQL script from more than 20 major database vendors.

### How to use SQLFlow
- Open [the official website](https://gudusoft.com/sqlflow/#/) of the SQLFlow and paste your SQL script or metadata to get a nice clean lineage diagram.
- Call the Restful API of the SQLFlow in your own code to get data lineage metadata decoded by the SQLFlow from the SQL script.
- The on-premise version of SQLflow enables you to use it on your own server to keep the data safer.


### The price plan
- [SQLFlow price plan](https://gudusoft.com)

### Restful APIs
- [SQLFlow API document](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md)
- [Client in C#](https://github.com/sqlparser/sqlflow_public/tree/master/api/client/csharp)

### SQLFlow architecture
- [Architecture document](sqlflow_architecture.md)

### User manual and FAQ
- [User guide](sqlflow_guide.md)
- [SQLFlow FAQ](sqlflow_faq.md)


