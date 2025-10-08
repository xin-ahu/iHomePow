

base_url = 'http://116.62.184.16/ihome-platform/prod-api'

login_url = f'{base_url}/user/apLogin'

payload = {
    "loginFrom": "web",
    "loginName": "13856947064",
    "password": "ZmVuZ3ppNjYxMA=="
}


header = {
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

pageNum = 1
pageSize = 10