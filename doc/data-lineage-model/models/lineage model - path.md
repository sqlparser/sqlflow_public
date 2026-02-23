## path

This is the path such as hdfs path, Amazon S3 path, BigQuery GS path.

struct definition

```json
{
    "elementName" : "path",
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
            "name": "uri",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "coordinate",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "columns",
            "typeName": "array<column>",
            "isOptional": true
        } 
    ]
}
```

### id

the unique id in the output.

### name

the name of the path.

### type

type of the path, one of `hdfs`, Amazon `s3`, BigQuery `GS`

### uri

the path where the object is stored.

### columns

Path doesn't has columns in fact. We add columns here in order to make path available in column-level lineage model by using the pseudo column.
