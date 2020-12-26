copy into mycsvtable
  from @my_csv_stage/tutorials/dataloading/contacts1.csv
  on_error = 'skip_file';
  
/*  
copy into mycsvtable
  from @my_csv_stage/tutorials/dataloading/
  pattern='.*contacts[1-5].csv'
  on_error = 'skip_file';
*/

copy into myjsontable
  from @my_json_stage/tutorials/dataloading/contacts.json
  on_error = 'skip_file';
  