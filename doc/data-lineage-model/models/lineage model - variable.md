## variable

the variable used in the SQL especially in the stored procedure.

struct definition

```json
{
    "elementName" : "variable",
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
            "name": "subType",
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

variable name in the original SQL query.

### type

This value is always be `type`

### subType

type of the variable, one of those values: `scalar`,`cursor`,`record`

### columns

Array of column name in the cursor/record variable. Or the variable name of the scalar variable.
