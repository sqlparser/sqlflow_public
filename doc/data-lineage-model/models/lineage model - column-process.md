## column-process

This is the business rule that convert column.

Struct definition

```json
{
    "elementName" : "column-process",
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
            "name": "dependency",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "targetColumn",
            "typeName": "integer",
            "isOptional": false
        },
        {
            "name": "sourceColumns",
            "typeName": "array<integer>",
            "isOptional": false
        },
        {
            "name": "reltions",
            "typeName": "array<integer>",
            "isOptional": false
        },
        {
            "name": "hashId",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "parentProcessId",
            "typeName": "int",
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

name of the column process.

### dependency

The lineage also captures the kind of dependency, as listed below:

* SIMPLE: output column has the same value as the input
* FUNCTION: output column is transformed by function.
* EXPRESSION: output column is transformed by some expression at runtime (for e.g. a Hive SQL expression) on the Input Columns.
* SCRIPT: output column is transformed by a user provided script.

### targetColumn

id of the target column.

### sourceColumns

array of the source column id.

### relations

The array of relations that made up of this column-process.

### hashId

The hashId is calculated based on the hashId of the relations that made up of this column-process.
