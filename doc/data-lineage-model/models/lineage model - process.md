## process

This is the SQL statement that transforms the data.

struct definition

```json
{
    "elementName" : "process",
    "attributeDefs": [
        {
            "name": "id",
            "typeName": "int",
            "isOptional": false,
            "isUnique": true
        },
        {
            "name": "name",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "type",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "queryHashId",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "procedureName",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "coordinate",
            "typeName": "string",
            "isOptional": false
        }
    ]
}
```

### id

the unique id in the output.

### name

name of the process.

### type

type of the process, usually, it's the type of SQL statement that do the data transformation. Available value:

* Create Table
* Create External Table
* Create View
* Create Stage
* Alter Table
* Update
* Merge
* Insert
* Select Into
* Hive Load

### queryHashId

This is the MD5 hash id that uniquely identify this SQL query. This `queryHashId` will be used when update a column or table-level lineage in the Atlas or other data catalog.

### procedureName

If this query statement is inside a stored procedure, this `procedureName` is the fully qualified name of the stored procedure. Otherwise, the `procedureName` should always be the `batchQueries`
