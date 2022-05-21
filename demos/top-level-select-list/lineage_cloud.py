import requests
import json
import pprint

# Please change the IP to the server where Gudu SQLFlow on-premise version is setup
sqlflow_cloud_server = 'https://api.gudusoft.com' 
sqlflow_generate_token = sqlflow_cloud_server + '/gspLive_backend/user/generateToken'
sqlflow_api = sqlflow_cloud_server + '/gspLive_backend/sqlflow/generation/sqlflow/graph'




# Please check here for detailed explanation of al parameters: https://github.com/sqlparser/sqlflow_public/tree/master/api/python/basic
userId = 'your user id here'
# This is your screct key: https://github.com/sqlparser/sqlflow_public/blob/master/sqlflow-userid-secret.md
screctKey = 'your secrect key here'  
dbvendor = 'dbvoracle'
ignoreRecordSet = 'True'
ignoreFunction = 'True'
showRelationType = 'fdd'
simpleOutput = 'False'
sqltext = """
select data.*, location.remote
from (
	select e.last_name, e.department_id, d.department_name
	from employees e
	left outer join department d
		on (e.department_id = d.department_id)
) data inner join
(
	select s.remote,s.department_id 
	from source s
	inner join location l 
	on s.location_id = l.id
) location on data.department_id = location.department_id;
"""

mapA = {'secretKey': screctKey, 'userId': userId}
header_dict = {"Content-Type": "application/x-www-form-urlencoded; charset=utf8"}
r = requests.post(sqlflow_generate_token, data=mapA, headers=header_dict)
rs = eval(r.text)
# print(rs)
tk = rs.get("token")

data = {'dbvendor': dbvendor, 'ignoreRecordSet': ignoreRecordSet, 'simpleOutput': simpleOutput,
        'showRelationType': showRelationType, 'token': tk, 'userId': userId, 'sqltext': sqltext}
datastr = json.dumps(data)
response = requests.post(sqlflow_api, data=eval(datastr))
jsonStr = response.json()

pp = pprint.PrettyPrinter(width=41, compact=True)
pp.pprint(jsonStr)
