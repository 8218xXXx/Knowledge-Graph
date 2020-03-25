# encoding=utf8
import urllib3
import json
from aip import AipNlp
from settings import baidu_access_token, baidu_app_id_nlp, baidu_app_key_nlp, baidu_access_token_nlp, pos_en_cn
from settings import qa_cookie
import json
url_template = 'https://aip.baidubce.com/rpc/2.0/kg/v1/cognitive/entity_annotation?access_token={}'


def get_baike_url(name):
    http = urllib3.PoolManager()
    data = {'data': name}
    encoded_data = json.dumps(data)
    url = url_template.format(baidu_access_token)
    response = http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})
    attrs = response.data.decode('utf-8')
    params = json.loads(attrs)
#    if len(params['entity_annotation']) == 0:
 #       return "www.baidu.com"
  #  print(params['entity_annotation'][0]['_bdbkUrl'])
   # return params['entity_annotation'][0]['_bdbkUrl']

def hello():
    client = AipNlp(appId=baidu_app_id_nlp, apiKey=baidu_app_key_nlp, secretKey=baidu_access_token_nlp)
    print(client.lexerCustom("北大确实是一所不错的学校"))

"""分词+词性"""
def lexer(statement):
    client = AipNlp(appId=baidu_app_id_nlp, apiKey=baidu_app_key_nlp, secretKey=baidu_access_token_nlp)
    reults = client.lexer(statement)
    print(reults)
    items = reults['items']
    print()
    contents = {}
    contents["type"] = "force"
    categories = []
    no_repeat_categories = set()
    for item in items:
        print(item)
        pos = item['ne'] or item['pos']
        no_repeat_categories.add(pos_en_cn[pos])
    print(no_repeat_categories)
    no_repeat_categories = list(no_repeat_categories)
    categories_to_int = {}
    cnt = 0
    for category in no_repeat_categories:
        node = {'name': category, 'keyword': {}, 'base': category}
        categories.append(node)
        categories_to_int[category] = cnt
        cnt += 1
    node = {'name': '文本语句', 'keyword': {}, 'base': '文本语句'}
    categories.append(node)
    categories_to_int['文本语句'] = cnt
    contents['categories'] = categories
    nodes = []
    links = []
    node = {'name': statement, 'value': statement, 'category': categories_to_int['文本语句']}
    nodes.append(node)
    cnt = 0
    print(categories_to_int)
    for item in items:
        word = item['item']
        print("word:",word)
        print(item['ne'])
        print(item['pos'])
        if item['pos'] == '':
            pos = item['ne']
        else:
            pos = item['pos']
        print("pos:",pos)
        node = {'name': word, 'value': str(word), 'category': categories_to_int[pos_en_cn[pos]]}
        link = {'source': 0, 'target': cnt + 1, 'value': pos_en_cn[pos]}
        print("node:",node)
        print("link:",link)
        nodes.append(node)
        links.append(link)
        cnt += 1
    contents['nodes'] = nodes
    contents['links'] = links
    return contents

"""情感分析"""
def emotion(statement):
    client = AipNlp(appId=baidu_app_id_nlp, apiKey=baidu_app_key_nlp, secretKey=baidu_access_token_nlp)
    positive = []
    negative = []
    neutral = []
    mydata = {}
    options = {}
    scenes = ['talk','task','customer_service']
    for scene in scenes:
        options["scene"] = scene
        results = client.emotion(statement, options)
        print(results)
        for item in results['items']:
            if item['label'] == 'neutral':
                neutral.append(item['prob'])
            elif item['label'] == 'pessimistic':
                negative.append(item['prob'])
            else:
                positive.append(item['prob'])
    mydata['positive'] = positive
    mydata['negative'] = negative
    mydata['neutral'] = neutral
    mydata['statement'] = statement
    print(mydata)
    return mydata

if __name__ == '__main__':
    get_baike_url('马云')

    # data = "{\"log_id\":\"UNITTEST_10000\",\"version\":\"2.0\",\"service_id\":\"S10000\",\"session_id\":\"\"," \
    #             "\"request\":{\"query\":\"你好.\",\"user_id\":\"88888\",\"dialog_state\":{\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"1057\"]}}"
    # data = "{\"serviceId\":\"S12664\",\"logId\":\"e3fb06e0-1a61-11e9-87b4-b5cd10620bad\",\"sessionId\":null,\"query\":\"赵本山的老婆是谁？\",\"sysRememberSkills\":[]}"
    # data = data.encode('utf-8')
    # rep = requests.post("https://ai.baidu.com/unit/v2/service/chat?access_token=24.f3a55f52acb95cb922d79805612470b0.2592000.1550324766.282335-15441387",
    #                      data=data, cookies={'Cookie':qa_cookie})
    # contents = json.loads(rep.content.decode("utf-8"))
    # print(contents['result']['responseList'][0])
    # for content in contents['result']['responseList']:
    #     print(content)
    # print(type(contents['result']['responseList'][0]))
    # result = contents['result']['responseList'][0]
    # print(result['actionList'][0]['say'])
