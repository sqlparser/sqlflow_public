## column

struct definition

```json
{
    "elementName" : "column",
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
            "isOptional": true
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

column name in the original SQL query.

### type

type of this column.

### `coordinate`

Indicates the positions of the occurences of the column in the SQL script.
