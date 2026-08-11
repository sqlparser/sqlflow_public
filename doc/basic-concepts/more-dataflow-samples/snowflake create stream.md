### create stream

```sql
create stream mystream on table mytable;
```

data lineage

```plaintext
mytable -> fdd -> mysteam
```

#### column level lineage

```plaintext
mytable.PseudoRows -> fdd -> mysteam.PseudoRows
```

#### table level lineage

```plaintext
mytable -> create stream process -> mystream
```

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> A stream definition is not a static copy. SLPC emits STREAM and TABLE endpoints,
> `ObjectRelationship(STREAMS_FROM)` with `BASE_RELATION=mytable`, and
> `StatementOperation(CREATE_STREAM, DEFINITION_ONLY)` with `CREATED_STREAM=mystream`. It does not emit
> `mytable -> mystream` as a VALUE fact unless an engine separately proves a concrete content dependency.
> A legacy projector may synthesize the old arrow only as a labeled compatibility view.

### sample SQLs

```sql
create stream mystream on table mytable before (timestamp => to_timestamp(40*365*86400));
create stream mystream on table mytable at (timestamp => to_timestamp_tz('02/02/2019 01:02:03', 'mm/dd/yyyy hh24:mi:ss'));
create stream mystream on table mytable at(offset => -60*5);
create stream mystream on table mytable before(statement => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726');

-- external table
-- Create an external table that points to the MY_EXT_STAGE stage.
-- The external table is partitioned by the date (in YYYY/MM/DD format) in the file path.
create external table my_ext_table (
  date_part date as to_date(substr(metadata$filename, 1, 10), 'YYYY/MM/DD'),
  ts timestamp as (value:time::timestamp),
  user_id varchar as (value:userId::varchar),
  color varchar as (value:color::varchar)
) partition by (date_part)
  location=@my_ext_stage
  auto_refresh = false
  file_format=(type=json);

-- Create a stream on the external table
create stream my_ext_table_stream on external table my_ext_table insert_only = true;
```


 ![image.png](https://images.gitee.com/uploads/images/2021/0826/104137_439fc6d3_8136809.png)

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> Each `CREATE STREAM ... AT/BEFORE` statement has the same `STREAMS_FROM` relationship and
> `CREATE_STREAM` operation; timestamp, offset, and statement selectors are statement evidence/literal
> inputs, not endpoint identity. The external-table statement is `CREATE_EXTERNAL_TABLE` with storage
> `READS_FROM` dependency. `my_ext_table_stream` is another STREAM endpoint with
> `STREAMS_FROM(my_ext_table)` and `CREATE_STREAM`; `insert_only` is typed operation/extension metadata.
> Every locator and literal follows secret-redaction rules.

### reference

[https://docs.snowflake.com/en/sql-reference/sql/create-stream.html](https://docs.snowflake.com/en/sql-reference/sql/create-stream.html)
