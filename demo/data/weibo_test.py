import requests

if __name__ == '__main__':
    r = requests.post('https://weibo.cn/find/user', data={'keyword': '张翼ZyzY'})
    print(r.content)