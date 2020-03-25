#coding=utf-8
import requests

if __name__ == '__main__':
    cookie = {
        "Cookie": '_T_WM=e1e85f1a27e03a5daa55091bcef73d67; MLOGIN=0; M_WEIBOCN_PARAMS=uicode%3D10000011%26fid%3D102803; SUB=_2A25xqAfEDeRhGeBG6FAU-S3Iyz-IHXVTUqmMrDV6PUJbkdAKLWrZkW1NRg0Gu1Yobj3b2IGF9wiQ_mBfWnUMqVK9; SUHB=0S7CM1qupy9gjg; SCF=Alh_hWHjS0b7iSwSB7L4cZcKm3v_-8575eYbj4B1ZKbveh9nDe5SUo8oh_hKJPObgIgYsk2FHEEva_fTgRvmdmc.; SSOLoginState=1554806676'
    }  # 将your cookie替换成自己的cookie
    username = "方滨兴"
    html = requests.post('https://weibo.cn/find/user', cookies=cookie, data={'keyword': username, 'suser': 2}).content
    print(html)