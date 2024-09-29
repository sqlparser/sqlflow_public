## procedure

Represents a stored procedure.

struct definition

```json
{
    "elementName" : "procedure",
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
            "name": "coordinate",
            "typeName": "string",
            "isOptional": false
        },  
        {
            "name": "arguments",
            "typeName": "array<argument>",
            "isOptional": true
        } 
    ]
}
```

### id

the unique id in the output.

### name

procedure name in the original SQL query.

### type

One of those values: `createprocedure`

### coordinate

Indicates the positions of the occurrences in the SQL script.

### argument

argument of the stored procedure

struct definition

```json
{
    "elementName" : "argument",
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
            "name": "datatype",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "coordinate",
            "typeName": "string",
            "isOptional": false
        },  
        {
            "name": "inout",
            "typeName": "string",
            "isOptional": true
        } 
    ]
}
```
