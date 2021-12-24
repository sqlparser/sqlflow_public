## Snowflake copy into table
[Official SQL syntax link for copy into table](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html#)

### internalStage

#### SQL 1
```sql
copy into mytable
from @my_int_stage;
```

The data lineage generated for this SQL:
```
@my_int_stage(unknownPath) -> mytable(*)
```
`unknownPath` and `*` is added by the gudu SQLFlow, and those columns are marked as `source="system"`.

#### SQL 2
```sql
copy into mytable
file_format = (type = csv);
```

No data lineage will be generated for this SQL due to the lack of FROM clause.

#### SQL 3
```sql
copy into mytable from @~/staged
file_format = (format_name = 'mycsv');
```

The data lineage generated for this SQL:
```
@~(staged) -> mytable(*)
```

`@~` represents a person stage.

### externalStage

#### SQL 1
```sql
copy into mycsvtable
  from @my_ext_stage/tutorials/dataloading/contacts1.csv;
```

The data lineage generated for this SQL:
```
file(/tutorials/dataloading/contacts1.csv) - > @my_ext_stage(unknownPath) -> mycsvtable(*)
```

  
#### SQL 2
```sql
create or replace stage my_csv_stage
  file_format = mycsvformat
  url = 's3://snowflake-docs';
  
copy into mycsvtable
  from @my_csv_stage/tutorials/dataloading/contacts1.csv
  on_error = 'skip_file';
```

The data lineage generated for this SQL:
```
file(/tutorials/dataloading/contacts1.csv) - > @my_csv_stage(s3://snowflake-docs) -> mycsvtable(*)
```

### externalLocation
#### SQL 1
```sql
copy into mytable
  from 's3://mybucket/data/files'
  storage_integration = myint
  encryption=(master_key = 'eSxX0jzYfIamtnBKOEOwq80Au6NbSgPH5r4BDDwOaO8=')
  file_format = (format_name = my_csv_format);  
```

The data lineage generated for this SQL:
```
directory('s3://mybucket/data/files') -> mytable(*)
```

