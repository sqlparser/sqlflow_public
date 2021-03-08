## use Curl to call SQLFlow API

The result is returned in JSON format.

### get metadata and data linege

https://api.gudusoft.com/gspLive_backend

- set the input sql inline
```
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow" -H  "accept:application/json;charset=utf-8" -H  "Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE"  -F "dbvendor=dbvoracle" -F "ignoreRecordSet=true" -F "sqltext=select name from user"
```

- set the input sql from a file
```
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow" -H  "accept:application/json;charset=utf-8" -H  "Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE"  -F "dbvendor=dbvoracle" -F "ignoreRecordSet=true" -F "sqlfile=@c:/tmp/test.sql"
```

### get the join

- set the input sql from a file
```
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow" -H  "accept:application/json;charset=utf-8" -H  "Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE"  -F "dbvendor=dbvmysql" -F "ignoreRecordSet=true" -F "showRelationType=join" -F "sqlfile=@c:/tmp/test.sql"
```

### More APIs
https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md


curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow" -H  "accept:application/json;charset=utf-8" -H  "Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYxMDEyMTYwMCwiaWF0IjoxNTc4NTg1NjAwfQ.9AAIkjZ3NF7Pns-hRjZQqRHprcsj1dPKHquo8zEp7jE"  -F "dbvendor=dbvoracle" -F "ignoreRecordSet=true" -F "sqltext=select name from user"