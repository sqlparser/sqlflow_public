## view

struct definition

```json
{
    "elementName" : "view",
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
            "name": "alias",
            "typeName": "string",
            "isOptional": true
        },
        {
            "name": "type",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "database",
            "typeName": "string",
            "isOptional": true
        },  
        {
            "name": "schema",
            "typeName": "string",
            "isOptional": true
        },  
        {
            "name": "processIds",
            "typeName": "int",
            "isOptional": true
        },
        {
            "name": "coordinate",
            "typeName": "string",
            "isOptional": true
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

unique id in the output.

### name

view name in the original SQL query.

### alias

alias of the view in the original SQL query.

### type

type of the view, available value: `view`

### processIds
