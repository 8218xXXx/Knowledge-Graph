max_nodes_per_level = 110  # 控制每层显示的邻居节点的个数
max_nodes = 160  # 控制路径搜索时，显示每层展示的邻居节点个数
sql_template = 'insert into relationship (source_user,target_user,trust_level) values("{}","{}","{}")'

source_template = '''
    select * from relationship where source_user="{}"
'''
all_template = '''
    select * from relationship where source_user="{}" and target_user="{}"
'''
target_template = '''
    select * from relationship where target_user="{}"
'''
user_profile_template = '''
    insert into weibo_user_profile (usernmame, user_id, weibo_num, following, follower) values("{}","{}","{}","{}","{}") 
'''

user_content_template = '''
    insert into weibo_user_content (usernmame, user_id, weibo_content, weibo_position, publish_time, up_num, repost_num, comment_num, publish_tool) 
    values("{}","{}","{}","{}","{}","{}","{}","{}","{}") 
'''

user_follow_template = '''
    insert into weibo_follow_user (username, user_id, follow_user_name, follow_user_link) values ("{}", "{}","{}","{}")
'''
entity_url = 'https://api.ownthink.com/kg/knowledge?entity={}'
mention_url = 'https://api.ownthink.com/kg/ambiguous?mention={}'
info_url = 'https://api.ownthink.com/bot?token=openbot&info={}'

level_to_int = {
    'Master': 1.0,
    'Journeyer': 0.75,
    'Apprentice': 0.5,
    'Observer': 0.25
}

boson_token = "mp08Nltk.31524.tClWZ2mZX4xF"

topic_to_id = {
    0: '体育',
    1: '教育',
    2: '财经',
    3: '社会',
    4: '娱乐',
    5: '军事',
    6: '国内',
    7: '科技',
    8: '互联网',
    9: '房产',
    10: '国际',
    11: '女性',
    12: '汽车',
    13: '游戏',
}

models = ['general', 'auto', 'kitchen', 'food', 'news', 'weibo']
model_to_name = {
    'general': '通用',
    'auto': '汽车',
    'food': '餐饮',
    'kitchen': '厨具',
    'news': '新闻',
    'weibo': '微博'
}

pos_en_cn = {
    'n':'普通名词',
    'nr':'人名',
    'nz':'其他专名',
    'a':'形容词',
    'm':'数量词',
    'c':'连词',
    'f':'方位名词',
    'ns':'地名',
    'v':'普通动词',
    'ad':'副形词',
    'q':'量词',
    'u':'助词',
    's':'处所名词',
    'nt':'机构团体名',
    'vd':'动副词',
    'an':'名形词',
    'r':'代词',
    'xc':'其他虚词',
    't':'时间名词',
    'nw':'作品名',
    'vn':'名动词',
    'd':'副词',
    'p':'介词',
    'w':'标点符号',
    'PER':'人名',
    'LOC':'地名',
    'ORG':'机构名',
    'TIME':'时间'
}

baidu_access_token = '24.024a11ea578c5eaccab31d7b4f6c3118.2592000.1587117936.282335-15340960'

baidu_app_id_nlp = '17527563'
baidu_app_key_nlp = 'UmI2pQbzmbhG2szIlggjBnHD'
baidu_access_token_nlp = 'g8HSm5uCoVCtGt9Dmbft7Cl19dX0hR5y'

#baidu_app_id_nlp = '15052604'
#baidu_app_key_nlp = '4F1hwLT9H5eHYyL4GWc4BRDK'
#baidu_access_token_nlp = 'FCZpazzkIxe1qCm7z3iU2oKbCjcs7XhP'

get_baidu_access_token = '''
https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=5RNfxsjDKpgRY1fw8DpMx1PS&client_secret=7xa2XHcTgtC1y3N2IbhBeKIGVe0piGDp
'''

baidu_kg_app_url = '''
https://console.bce.baidu.com/ai/?fromai=1#/ai/kg/app/list
'''

cookie = {
        "Cookie": '_T_WM=6b09d8cfff99c3af3cc10ca0a518754a; MLOGIN=0; M_WEIBOCN_PARAMS=uicode%3D10000011%26fid%3D102803; SUB=_2A25xD7_ADeRhGeBG6FAU-S3Iyz-IHXVS88GIrDV6PUJbkdANLRb1kW1NRg0GuxMN95p1EYHz8xkVaR_F31UftZz0; SUHB=0JvgFbIGwbi-V5; SCF=An4qs1Vf3I7EPiars1HvEpFDil3QE3JZUgkP-z-qsCp99-Lpz68LeicTHyR37xjm_vpuCsryN-R519wxrK1NLYA.; SSOLoginState=1544277904'
}  # 将your cookie替换成自己的cookie

# mysql_password =  'Threat-Mysql-222'
mysql_password =  'qwertasdfg0215'

follows_limit = 50
weibo_contents_limit = 40


relationship_list = [
    '老公',
    '现任老公'
    '前任老公',
    '丈夫',
    '现任丈夫',
    '前任丈夫',
    '前任妻子',
    '前任老婆',
    '老婆',
    '现任妻子',
    '现任老婆',
    '妻子',
    '前妻',
    '前夫',
    '好友',
    '朋友',
    '学生',
    '毕业院校',
    '毕业学校'
    '女朋友',
    '女友',
    '前女友',
    '前男友',
    '男朋友',
    '男友',
    '父亲',
    '爸爸',
    '母亲',
    '妈妈',
    '父母',
    '女儿',
    '儿子',
    '孩子',
    '小孩',
    '亲人',
    '前任',
    '配偶',
    '夫人',
    '副总统',
    '儿女',
]
qa_url =  "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=24.3edc143a3b2db586ea9f2636ea0dd953.2592000.1573714494.282335-17530219"
#qa_url =  "https://ai.baidu.com/unit/v2/service/chat?access_token=24.3edc143a3b2db586ea9f2636ea0dd953.2592000.1573714494.282335-17530219"

qa_params = '{"serviceId":"S12664","logId":"e3fb06e0-1a61-11e9-87b4-b5cd10620bad","sessionId":"123","query":"%s","sysRememberSkills":["31684"]}'

#qa_params = '{"serviceId":"S12664","logId":"e3fb06e0-1a61-11e9-87b4-b5cd10620bad","sessionId":null,"query":"%s","sysRememberSkills":["31684"]}'

#qa_cookie = "BAIDUID=5DC64D03384232FE4701DADEFD981905:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2145916555; path=/; domain=.baidu.com; version=1"

qa_cookie = "BAIDUID=B10CB08582F6171B7009ADABE7110ABB:FG=1; PSTM=1544792524; BIDUPSID=9C88F25CAAFBDAA127FB0EACDB62EA0B; __cfduid=d3c2dd86b5ea2ad73e2ac17ae9971251c1544865136; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-158%3A131%3A; BDSFRCVID=Jz8sJeCCxG3ZpL69h9PqSyR0pOdgXga64J203J; H_BDCLCKID_SF=tR3KB6rtKRTffjrnhPF35Mu3KP6-3MJO3b7ZbKoKfRjheKbP5l_aM-v3bGrnW-jd-DrBohFLtDL-hIDCe5u35n-WqxRt54cB2CTeXjrJabC3JfcVXU6qLT5X0xvgLlFefCbZM-nFanQfsJK404oj5l0njxQy2f3gJG5b2Uc_KlnRJ4Tb3xonDh88bG7MJUntKDnPLx5O5hvvhb6O3M7-qfKmDloOW-TB5bbPLUQF5l8-sq0x05bke6oWeH-OqT-sb4o2LPoV-TrjDnCrXt5hKUI8LPbO05JZBanqVRP5a4D5jbo3hPrlbh_BbxriQlcAt2LEoC0XtCIbbKv65nt_-tFX-U702t_XKKOLsJO8fMPVEtO_bfbT2MbyWl3rtjc3JKoWVUcEtfn-eb3ybPL-jMTXDabZqj_ffRC8_KPQb-3bKRjYK4bsMtC_qxby2C62aJ3yalObWJ5TEPnjDp62X55-MatOQpoeWCnCLJbjyn3HMCb_D605y6TLjNueqTkff5IX3-b-24t_Hn7zepno0btpbtbmhU-eWeOnLDTS2CbM8-bjjTrE3t0u5xj0BhokWR7ZVDD5fCDBMIPr5nJbq4_tKxb3a46KHD7yW6rJaDvRsRvRy4oTLnk1Dn6jWTK82NQNKl5eyC56MnbTW-JHj60pDG0eBjIDJbKeVIP5f-K_HPb4MJ0_-P4DenQtBRJZ5m7mXp0bWq7xfCTdK4orDPDJhxnUL43IbDc0aMjwWCOkbC8xe5ubj65M5pJfetJeKC5HsJOOaCvlSIbRy4oTLnk1DP6g-fI82nKfoKoSB565bhjejJ6G3lksK4PeBjIDJbKDVC0yf-3bfTrpMJ5jM-FH-eT22-uXKK_satFy-hcqEpO9QTbAKM7BefA8QnogMGujQp7e5MnJHDLmy6K2DUTh-p52f6_Dtb6P; delPer=0; PSINO=7; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; pgv_pvi=8843904000; pgv_si=s2592886784; Hm_lvt_8b973192450250dd85b9011320b455ba=1546568875,1546568957,1546569123,1547732095; PHPSESSID=9f4n42cadialu529buf6lseij2; BDUSS=hVWXRkdFVNb0VhUlFZRjRFdU56bnZ3U1RnU0NhbkdoUklvZWFSRmZmZHRFbWhjQUFBQUFBJCQAAAAAAAAAAAEAAABBw8qkU2hhbm5vbjc2NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG2FQFxthUBcVW; docVersion=0; H_PS_PSSID=26525_1433_21120_18560_28329_28131_26350_28266; seccode=74cfbd6c62f59b08fdea6c00b5e3384d; Hm_lpvt_8b973192450250dd85b9011320b455ba=1547734323"
if __name__ == '__main__':
    a = 1
    b = 2
    print(a/b)
