

# base_url = 'http://116.62.184.16/ihome-platform/prod-api'   # 测试环境
base_url = 'http://47.98.166.97/ihome-platform/prod-api'  # 生产环境

base_url_app = 'https://ihomepow-test.sungrowplant.com'

login_url = f'{base_url}/user/apLogin'

login_url_app = f'{base_url_app}/admin/user/apLogin'

payload = {
    "loginFrom": "web",
    "loginName": "13856947064",
    "password": "ZmVuZ3ppNjYxMA=="
}

payload_app = {
    "loginFrom": "mini",
    "loginName": "13739284692",
    "password": "QTEyMzQ1Njc4"
}


header = {
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

header_app = {
    'Host': 'ihomepow-test.sungrowplant.com',
    'content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1 wechatdevtools/1.06.2401020 MicroMessenger/8.0.5 Language/zh_CN webview/'
}

pageNum = 1
pageSize = 10