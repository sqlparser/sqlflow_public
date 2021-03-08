# SQLFlow Python API Document

A tutorial for using the Python version of the SQLFlow API.

### GenerateTokenDemo.py

This demo shows how to get a token from a SQLFlow system that can be used to legally call other interfaces.

* Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **userSecret**: the userSecret of sqlflow client request. sqlflow web, required false, sqlflow client, required true

This is the user id that is used to connect to the SQLFlow server.
Always set this value to `gudu|0123456789` and keep `userSecret` empty if you use the SQLFlow on-premise version.

If you want to connect to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com), you may [request a 30 days premium account](https://www.gudusoft.com/request-a-premium-account/) to 
[get the necessary userId and secret code](/sqlflow-userid-secret.md).

### GenerateDataLineageDemo.py

This demo shows how to get the desired SQL script analysis results from the SQLFlow system.

* Parameters: 
    * **userId**: the user id of sqlflow web or client, required **true** 
    * **userSecret**: the userSecret of sqlflow client request. sqlflow web, required false, sqlflow client, required true
    * sqltext: sql text, required false
    * sqlfile: sql file, required false
    * **dbvendor**: database vendor, required **true**, available values: 
      * dbvbigquery, dbvcouchbase,dbvdb2,dbvgreenplum,dbvhana,dbvhive,dbvimpala,dbvinformix,dbvmdx,dbvmysql,dbvnetezza,dbvopenedge,dbvoracle,dbvpostgresql,dbvredshift,dbvsnowflake,dbvmssql,dbvsybase,dbvteradata,dbvvertica
    * showRelationType: show relation type, required false, default value is **fdd**, multiple values seperated by comma like fdd,frd,fdr. Available values: 
      * **fdd**: value of target column from source column
      * **frd**: the recordset count of target column which is affect by value of source column
      * **fdr**: value of target column which is affected by the recordset count of source column
      * **join**: combine rows from two or more tables, based on a related column between them
    * simpleOutput: whether simple output relation, required false, default value is false
    * ignoreRecordSet: whether ignore the record set, required false, default value is false
