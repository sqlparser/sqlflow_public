## Snowflake copy into location
[Official SQL syntax link for copy into location](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html)

### internalStage

#### SQL 1
```sql
copy into @%orderstiny/result/data_
  from orderstiny file_format = (format_name ='myformat' compression='GZIP');
```

The data lineage generated for this SQL:
```
orderstiny(*) -> orderstiny(result/data_)
```

`orderstiny(result/data_)` is the stage.

#### SQL 2
```sql
copy into @my_stage/result/data_ from (select * from orderstiny)
   file_format=(format_name='myformat' compression='gzip');
```

The data lineage generated for this SQL:
```
orderstiny(*) -> my_stage(result/data_)
```

#### SQL 3, personal stage
```sql
copy into @~ from home_sales
file_format=(type=csv null_if = ('NULL', 'null')
empty_field_as_null=false);
```

The data lineage generated for this SQL:
```
home_sales(*) -> ~(unknownPath)
```

### externalStage

#### SQL 1
```sql
copy into 's3://mybucket/unload/'
  from mytable
  storage_integration = myint
  file_format = (format_name = my_csv_format);
```

The data lineage generated for this SQL:
```
directory(s3://mybucket/unload/) -> mytable(*)
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
file(/tutorials/dataloading/contacts1.csv) - > my_csv_stage(s3://snowflake-docs) -> mycsvtable(*)
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

### Partitioning Unloaded Rows to Parquet Files
```sql
create or replace table t1 (
  dt date,
  ts time
  )
as
  select to_date($1)
        ,to_time($2)
    from values
           ('2020-01-28', '18:05')
          ,('2020-01-28', '22:57')
          ,('2020-01-28', null)
          ,('2020-01-29', '02:15')
;

copy into @%t1
  from t1
  partition by ('date=' || to_varchar(dt, 'YYYY-MM-DD') || '/hour=' || to_varchar(date_part(hour, ts))) -- Concatenate labels and column values to output meaningful filenames
  file_format = (type=parquet)
  max_file_size = 32000000
  header=true;
```

The data lineage generated for this SQL:
```
t1(dt,ts) -> %t1(unknownPath)
```

