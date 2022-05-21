import requests
import json
import pprint

# Please change the IP to the server where Gudu SQLFlow on-premise version is setup
sqlflow_on_premise_server = 'http://101.43.8.206:8081' 
sqlflow_api = sqlflow_on_premise_server + '/gspLive_backend/sqlflow/generation/sqlflow/graph'

# Please check here for detailed explanation of al parameters: https://github.com/sqlparser/sqlflow_public/tree/master/api/python/basic
userId = 'gudu|0123456789'
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


data = {'dbvendor': dbvendor, 'ignoreRecordSet': ignoreRecordSet, 'simpleOutput': simpleOutput,
        'showRelationType': showRelationType, 'userId': userId, 'sqltext': sqltext}
datastr = json.dumps(data)
response = requests.post(sqlflow_api, data=eval(datastr))
jsonStr = response.json()
# print(jsonStr)

pp = pprint.PrettyPrinter(width=41, compact=True)
pp.pprint(jsonStr)
