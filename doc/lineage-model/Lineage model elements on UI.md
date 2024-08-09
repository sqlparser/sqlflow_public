lineage model elements on UI

## Entity

path in the json:  `data->sqlflow->dbobjs`

### 1. Permanent entity

#### 1. table

![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/191609_0668124e_8136809.png "屏幕截图.png")

#### 2. external table

#### 3. view

![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/191722_f1de58a0_8136809.png "屏幕截图.png")

#### 4. hive local directory/inpath (type is path)

```sql
LOAD DATA INPATH '/user/data/pv_2008-06-08_us.txt' INTO TABLE page_view PARTITION(date='2008-06-08', country='US')
```

![输入图片说明](https://images.gitee.com/uploads/images/2021/0620/001315_8bb5cd3c_8136809.png "屏幕截图.png")

#### 5. snowflake stage and path

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

![image.png](https://images.gitee.com/uploads/images/2021/0727/180953_b6445883_8136809.png)

#### 6. bigquery file uri(type is path)

```sql
CREATE EXTERNAL TABLE dataset.CsvTable OPTIONS (
  format = 'CSV',
  uris = ['gs://bucket/path1.csv', 'gs://bucket/path2.csv']
);
```

BigQuery create external table:
![输入图片说明](https://images.gitee.com/uploads/images/2021/0620/000802_4c090d22_8136809.png "屏幕截图.png")

### 2. temporary entity

#### 1. select_list

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/191530_b174d7df_8136809.png "屏幕截图.png")

#### 2. merge_insert

```sql
-- bigquery sample SQL
MERGE dataset.DetailedInventory T
USING dataset.Inventory S
ON T.product = S.product
WHEN NOT MATCHED AND s.quantity < 20 THEN
  INSERT(product, quantity, supply_constrained, comments)
  VALUES(product, quantity, true, ARRAY<STRUCT<created DATE, comment STRING>>[(DATE('2016-01-01'), 'comment1')])
WHEN NOT MATCHED THEN
  INSERT(product, quantity, supply_constrained)
  VALUES(product, quantity, false)
;
```

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/191107_8968ae0a_8136809.png "屏幕截图.png")

#### 3. merge_update

```sql
-- couchbase
MERGE INTO all_empts a USING emps_deptb b ON KEY b.empId
WHEN MATCHED THEN
     UPDATE SET a.depts = a.depts + 1,
     a.title = b.title || ", " || b.title
WHEN NOT MATCHED THEN
     INSERT  { "name": b.name, "title": b.title, "depts": b.depts, "empId": b.empId, "dob": b.dob }
```

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/192035_de80e094_8136809.png "屏幕截图.png")

#### 4. update_set

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/213231_ac0d23ec_8136809.png "屏幕截图.png")

#### 5. update-select

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/213021_f18c731d_8136809.png "屏幕截图.png")

#### 6. insert-select

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/213658_6300b209_8136809.png "屏幕截图.png")

#### 7. function

In order to show the function in the result, please turn on this setting:

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/234638_578c62bb_8136809.png "屏幕截图.png")

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/234222_d5dbc796_8136809.png "屏幕截图.png")

#### 8. union

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/214736_2bd5f7e1_8136809.png "屏幕截图.png")

#### 9. cte

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/214239_8bd93fc3_8136809.png "屏幕截图.png")

#### 10. pivot table

![输入图片说明](https://images.gitee.com/uploads/images/2021/0619/235133_d683d625_8136809.png "屏幕截图.png")

#### 11. snowflake pivot alias

![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/200339_c6e02fef_8139001.png "屏幕截图.png")

#### 12. mssql open json

![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/201042_fa146c15_8139001.png "屏幕截图.png")

#### 13. mssql json property

![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/201357_0b1297e2_8139001.png "屏幕截图.png")

## relationship

path in the json: `data->sqlflow->relations`

#### 1. fdd, data flow

![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/192123_cd45caaf_8136809.png "屏幕截图.png")

#### 2. fdr, frd data impact

dash line

![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/192342_469b7474_8136809.png "屏幕截图.png")

#### 3. join

dash line

![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/201812_e60c597c_8139001.png "屏幕截图.png")
