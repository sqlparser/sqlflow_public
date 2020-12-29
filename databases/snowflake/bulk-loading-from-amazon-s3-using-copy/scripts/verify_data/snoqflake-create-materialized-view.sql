create materialized view exttable_csv_mv
  as
  select ID , LAST_NAME , FIRST_NAME ,COMPANY,EMAIL  from mycsvtable;
  
create materialized view exttable_json_mv
  as
  select * from myjsontable;  