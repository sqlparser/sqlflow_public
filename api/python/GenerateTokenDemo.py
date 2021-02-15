import requests

import json

if __name__ == '__main__':

    url = 'https://api.gudusoft.com/gspLive_backend/user/generateToken'

    # the user id of sqlflow web or client, required true
    userId = ''

    # the secret key of sqlflow user for webapi request, required true
    screctKey = ''

    mapA = {'secretKey': screctKey, 'userId': userId}
    header_dict = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(url, data=mapA, headers=header_dict)

    print(r.text)
