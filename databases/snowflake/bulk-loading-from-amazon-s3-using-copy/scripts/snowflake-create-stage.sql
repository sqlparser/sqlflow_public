create or replace stage my_csv_stage
  file_format = mycsvformat
  url = 's3://snowflake-docs';
  
create or replace stage my_json_stage
  file_format = myjsonformat
  url = 's3://snowflake-docs';

create or replace stage external_stage
  file_format = mycsvformat
  url = 's3://private-bucket'
  storage_integration = myint;  