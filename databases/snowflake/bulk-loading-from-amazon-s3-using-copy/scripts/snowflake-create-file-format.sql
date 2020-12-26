create or replace file format mycsvformat
  type = 'CSV'
  field_delimiter = '|'
  skip_header = 1;
  
  
create or replace file format myjsonformat
  type = 'JSON'
  strip_outer_array = true;  