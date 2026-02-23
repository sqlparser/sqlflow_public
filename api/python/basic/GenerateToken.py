import requests

import json

def getToken(userId, server, port, screctKey):
    if userId == 'gudu|0123456789':
        return 'token'
    url = '/api/gspLive_backend/user/generateToken'
    if 'api.gudusoft.com' in server:
        url = '/gspLive_backend/user/generateToken'
    if port != '':
        url = server + ':' + port + url
    else:
        url = server + url
    mapA = {'secretKey': screctKey, 'userId': userId}
    header_dict = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        r = requests.post(url, data=mapA, headers=header_dict, verify=False)
    except Exception as e:
        print('get token failed.', e)
    result = json.loads(r.text)

    if result['code'] == '200':
        return result['token']
    else:
        print(result['error'])


if __name__ == '__main__':

    server = ''

    port = ''

    # the user id of sqlflow web or client, required true
    userId = ''

    # the secret key of sqlflow user for webapi request, required true
    screctKey = ''

    token = getToken(userId, server, port, screctKey)

    print(token)
