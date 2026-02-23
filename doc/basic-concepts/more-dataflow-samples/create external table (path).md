create table external table usually will use `path` object.

### snowflake create external

```sql
create or replace stage exttable_part_stage
  url='s3://load/encrypted_files/'
  credentials=(aws_key_id='1a2b3c' aws_secret_key='4x5y6z')
  encryption=(type='AWS_SSE_KMS' kms_key_id = 'aws/key');

create external table exttable_part(
 date_part date as to_date(split_part(metadata$filename, '/', 3)
   || '/' || split_part(metadata$filename, '/', 4)
   || '/' || split_part(metadata$filename, '/', 5), 'YYYY/MM/DD'),
 timestamp bigint as (value:timestamp::bigint),
 col2 varchar as (value:col2::varchar))
 partition by (date_part)
 location=@exttable_part_stage/logs/
 auto_refresh = true
 file_format = (type = parquet);
```

The data of the external table `exttable_part` comes from the `path ('s3://load/encrypted_files/')` via the stage: `exttable_part_stage`

```
path('s3://load/encrypted_files/') -> fdd -> exttable_part_stage (url) -> fdd -> exttable_part(date_part,timestamp,col2) 
```

#### dataflow in xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dlineage>
    <stage id="5" name="exttable_part_stage" type="stage" processIds="6" coordinate="[1,25,0],[1,44,0]">
        <column id="7" name="s3://load/encrypted_files/" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </stage>
    <path id="2" name="'s3://load/encrypted_files/'" uri="'s3://load/encrypted_files/'" type="path" coordinate="[-1,-1,0],[-1,-1,0]">
        <column id="3" name="s3://load/encrypted_files/" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </path>
    <process id="6" name="Query Create Stage" type="Create Stage" coordinate="[1,1,0],[4,58,0]"/>
    <process id="13" name="Query Create External Table" type="Create External Table" coordinate="[6,1,0],[15,33,0]"/>
    <table id="9" name="exttable_part" type="table" processIds="13" coordinate="[6,23,0],[6,36,0]">
        <column id="10" name="date_part" coordinate="[7,2,0],[7,11,0]"/>
        <column id="11" name="timestamp" coordinate="[10,2,0],[10,11,0]"/>
        <column id="12" name="col2" coordinate="[11,2,0],[11,6,0]"/>
    </table>
    <relation id="1" type="fdd">
        <target id="7" column="'s3://load/encrypted_files/'" parent_id="5" parent_name="exttable_part_stage" coordinate="[-1,-1,0],[-1,-1,0]"/>
        <source id="3" column="'s3://load/encrypted_files/'" parent_id="2" parent_name="'s3://load/encrypted_files/'" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </relation>
    <relation id="2" type="fdd">
        <target id="10" column="date_part" parent_id="9" parent_name="exttable_part" coordinate="[7,2,0],[7,11,0]"/>
        <source id="7" column="'s3://load/encrypted_files/'" parent_id="5" parent_name="exttable_part_stage" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </relation>
    <relation id="3" type="fdd">
        <target id="11" column="timestamp" parent_id="9" parent_name="exttable_part" coordinate="[10,2,0],[10,11,0]"/>
        <source id="7" column="'s3://load/encrypted_files/'" parent_id="5" parent_name="exttable_part_stage" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </relation>
    <relation id="4" type="fdd">
        <target id="12" column="col2" parent_id="9" parent_name="exttable_part" coordinate="[11,2,0],[11,6,0]"/>
        <source id="7" column="'s3://load/encrypted_files/'" parent_id="5" parent_name="exttable_part_stage" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </relation>
</dlineage>
```

#### diagam

![image.png](https://images.gitee.com/uploads/images/2021/0709/113955_8d0a8d6d_8136809.png)

#### table-level lineage

this SQL is able to create a table-level lineage like this:

```
path('s3://load/encrypted_files/') -> process(create stage) -> exttable_part_stage (url) -> process(create external table) -> exttable_part
```

![image.png](https://images.gitee.com/uploads/images/2021/0709/114036_31ac2c6c_8136809.png)

### bigquery create external table

```sql
CREATE EXTERNAL TABLE dataset.CsvTable OPTIONS (
  format = 'CSV',
  uris = ['gs://bucket/path1.csv', 'gs://bucket/path2.csv']
);
```

The data of the external table `dataset.CsvTable` comes from the csv file: `gs://bucket/path1.csv, gs://bucket/path2.csv`

```
path (uri='gs://bucket/path1.csv')  -> fdd ->  dataset.CsvTable
path (uri='gs://bucket/path2.csv')  -> fdd ->  dataset.CsvTable
```

#### dataflow in xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dlineage>
    <path id="6" name="'gs://bucket/path1.csv'" uri="'gs://bucket/path1.csv'" type="path" fileFormat="CSV" coordinate="[-1,-1,0],[-1,-1,0]">
        <column id="7" name="uri='gs://bucket/path1.csv'" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </path>
    <path id="9" name="'gs://bucket/path2.csv'" uri="'gs://bucket/path2.csv'" type="path" fileFormat="CSV" coordinate="[-1,-1,0],[-1,-1,0]">
        <column id="10" name="uri='gs://bucket/path2.csv'" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </path>
    <process id="3" name="Query Create External Table" type="Create External Table" coordinate="[1,1,0],[4,3,0]"/>
    <table id="2" schema="dataset" name="dataset.CsvTable" type="table" processIds="3" coordinate="[1,23,0],[1,39,0]">
        <column id="4" name="*" coordinate="[1,1,0],[1,2,0]"/>
        <column id="4_0" name="URI='GS://BUCKET/PATH1.CSV'" coordinate="[1,1,0],[1,2,0]"/>
        <column id="4_1" name="URI='GS://BUCKET/PATH2.CSV'" coordinate="[1,1,0],[1,2,0]"/>
    </table>
    <relation id="1" type="fdd">
        <target id="4" column="*" parent_id="2" parent_name="dataset.CsvTable" coordinate="[1,1,0],[1,2,0]"/>
        <source id="7" column="uri='gs://bucket/path1.csv'" parent_id="6" parent_name="'gs://bucket/path1.csv'" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </relation>
    <relation id="2" type="fdd">
        <target id="4" column="*" parent_id="2" parent_name="dataset.CsvTable" coordinate="[1,1,0],[1,2,0]"/>
        <source id="10" column="uri='gs://bucket/path2.csv'" parent_id="9" parent_name="'gs://bucket/path2.csv'" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </relation>
</dlineage>
```

#### diagam

![image.png](https://images.gitee.com/uploads/images/2021/0709/114123_8e3102c6_8136809.png)

#### table-level lineage

This SQL is able to create a table-level lineage like this:

```
path (uri='gs://bucket/path1.csv')  -> query process(create external table) ->  dataset.CsvTable
path (uri='gs://bucket/path2.csv')  -> query process(create external table) ->  dataset.CsvTable
```

![image.png](https://images.gitee.com/uploads/images/2021/0709/114151_76369339_8136809.png)

### Hive load data

```sql
LOAD DATA LOCAL INPATH /tmp/pv_2008-06-08_us.txt INTO TABLE page_view PARTITION(date='2008-06-08', country='US')
```

The data flow is:

```
path (uri='/tmp/pv_2008-06-08_us.txt')  ->  fdd -> page_view(date,country)
```

#### dataflow in xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dlineage>
    <path id="2" name="/tmp/pv_2008-06-08_us.txt " uri="/tmp/pv_2008-06-08_us.txt " type="path" coordinate="[1,24,0],[1,50,0]">
        <column id="3" name="uri=/tmp/pv_2008-06-08_us.txt " coordinate="[-1,-1,0],[-1,-1,0]"/>
    </path>
    <process id="6" name="Query Hive Load" type="Hive Load" coordinate="[1,1,0],[1,113,0]"/>
    <table id="5" name="page_view" type="table" processIds="6" coordinate="[1,61,0],[1,113,0]">
        <column id="7" name="date" coordinate="[1,81,0],[1,85,0]"/>
        <column id="8" name="country" coordinate="[1,100,0],[1,107,0]"/>
    </table>
    <relation id="1" type="fdd">
        <target id="7" column="date" parent_id="5" parent_name="page_view" coordinate="[1,81,0],[1,85,0]"/>
        <source id="3" column="uri=/tmp/pv_2008-06-08_us.txt " parent_id="2" parent_name="/tmp/pv_2008-06-08_us.txt " coordinate="[-1,-1,0],[-1,-1,0]"/>
    </relation>
    <relation id="2" type="fdd">
        <target id="8" column="country" parent_id="5" parent_name="page_view" coordinate="[1,100,0],[1,107,0]"/>
        <source id="3" column="uri=/tmp/pv_2008-06-08_us.txt " parent_id="2" parent_name="/tmp/pv_2008-06-08_us.txt " coordinate="[-1,-1,0],[-1,-1,0]"/>
    </relation>
</dlineage>
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0709/114357_f3be8f9f_8136809.png)

#### table-level lineage

```
path (uri='/tmp/pv_2008-06-08_us.txt')  -> query process(load data) -> page_view
```

![image.png](https://images.gitee.com/uploads/images/2021/0709/114422_58785e85_8136809.png)
