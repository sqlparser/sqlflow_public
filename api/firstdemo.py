"""
How to get user_id and secret_key: https://docs.gudusoft.com/3.-api-docs/prerequisites#generate-account-secret

once you have user_id and secret_key, 

user_id: <YOUR USER ID HERE>
secret_key: <YOUR SECRET KEY HERE>

you can get token by:

curl -X POST "https://api.gudusoft.com/gspLive_backend/user/generateToken" -H  "Request-Origion:testClientDemo" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:application/x-www-form-urlencoded;charset=UTF-8" -d "secretKey=YOUR SECRET KEY" -d "userId=YOUR USER ID HERE"

and then you can use the token to call the api:
curl -X POST "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow?showRelationType=fdd" -H  "Request-Origion:testClientDemo" -H  "accept:application/json;charset=utf-8" -H  "Content-Type:multipart/form-data" -F "sqlfile=" -F "dbvendor=dbvoracle" -F "ignoreRecordSet=false" -F "simpleOutput=false" -F "sqltext=CREATE VIEW vsal  as select * from emp" -F "userId=YOUR USER ID HERE"  -F "token=YOUR TOKEN HERE"

"""

# Python code to call the API based on the description:

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to get the token
def get_token(user_id, secret_key):
    url = "https://api.gudusoft.com/gspLive_backend/user/generateToken"
    headers = {
        "Request-Origion": "testClientDemo",
        "accept": "application/json;charset=utf-8",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    data = {
        "secretKey": secret_key,
        "userId": user_id
    }
    response = requests.post(url, headers=headers, data=data, verify=False, proxies=None)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Parse the JSON response
    json_response = response.json()
    
    # Check if 'token' key exists directly in the response
    if 'token' in json_response:
        return json_response['token']
    else:
        raise ValueError("Token not found in the response.")

# Function to call the SQLFlow API
def call_sqlflow_api(user_id, token, sql_text):
    url = "https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow?showRelationType=fdd"
    headers = {
        "Request-Origion": "testClientDemo",
        "accept": "application/json;charset=utf-8"
    }
    data = {
        "sqlfile": "",
        "dbvendor": "dbvoracle",
        "ignoreRecordSet": "false",
        "simpleOutput": "false",
        "sqltext": sql_text,
        "userId": user_id,
        "token": token
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Example usage
# How to get user_id and secret_key: https://docs.gudusoft.com/3.-api-docs/prerequisites#generate-account-secret

user_id = "your user id"
secret_key = "your secret key"
sql_text = "CREATE VIEW vsal AS SELECT * FROM emp"

try:
    # Get the token
    token = get_token(user_id, secret_key)
    print("Token:", token)
except requests.exceptions.RequestException as e:
    print("Error making request:", e)
except ValueError as e:
    print("Error parsing response:", e)

# Call the SQLFlow API
result = call_sqlflow_api(user_id, token, sql_text)
print(result)