
base_url = 'https://ihomepow-test.sungrowplant.com'

login = f'{base_url}/admin/user/apLogin'
payload = {"loginFrom": "mini", "loginName": "13739284692", "password": "QTEyMzQ1Njc4"}


login1 = f'{base_url}/admin-dev/user/apLogin'
payload1 = {"loginFrom": "mini", "loginName": "18851661678", "password": "QTEyMzQ1Njc4"}


headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1 wechatdevtools/1.06.2407120 MicroMessenger/8.0.5 Language/zh_CN webview/'
}
