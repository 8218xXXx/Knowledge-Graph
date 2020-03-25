# encoding=utf8
from flask import Flask
from flask import render_template, request
from datetime import timedelta
from util.utils import mention2entity, advogato_data_KG_target, get_paths, \
    advogato_data_KG_source, get_page_rank, KG_View_2,generate_lxy_contents
import json
import os, requests
from settings import qa_cookie,qa_params,qa_url
from util.baidu import get_baike_url, lexer, emotion
from util.weibo_util import generate_weibo_user_graph, get_weibo_userid,save_weibo_info, get_weibo_userid_special
from util.utils import get_trust_value, get_trust_value_1
from util.freebase import get_entity_name, get_freebase_info, test
from util.zhishi import get_related_urls
app = Flask(__name__)
app.config['debug'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
from numpy import float32


@app.route("/littlechongchong")
def littlechongchong():
    info = request.args.to_dict().get('info', '')
    data = qa_params % info
    data = data.encode('UTF-8')
    rep = requests.post(
        qa_url,
        data=data, cookies={'Cookie': qa_cookie})
    contents = json.loads(rep.content.decode("UTF-8"))
    print(contents)
    print(contents['result']['responseList'][0])
    for content in contents['result']['responseList']:
        print(content)
    print(type(contents['result']['responseList'][0]))
    result = contents['result']['responseList'][0]
    print(result['actionList'][0]['say'])
    return result['actionList'][0]['say']

@app.route('/about')
def about():
    return render_template('new_year.html')

@app.route('/weibo_search')
def weibo_search():
    return render_template('weibo_search.html')

@app.route('/news')
def news():
    return '敬请期待'

@app.route('/')
def hello_world():
    # return render_template('weibo_search.html')
    # return render_template('sentiment.html')
    return render_template('index1.html')
    # return render_template('nlp.html')
    # return render_template('attack_earth.html')

@app.route('/attribute')
def get_attribute():
    pairs = {}
    pairs['1'] = 1
    pairs['2'] = 2
    print(pairs)
    return json.dumps(pairs)

@app.route('/evaluation_2')
def page_rank_2():
    return render_template('page_rank_2.html')

@app.route('/evaluation')
def show_evaluation_results():
    return render_template('page_rank.html')

@app.route('/demo')
def show_demo():
    print("请求方式为:", request.method)
    entity = request.args.to_dict().get('entity', '')
    # mention = request.args.to_dict().get('mention','')
    if entity == '':
        return "请确定要查询的功能!"
    elif "ad_social:" in entity:
        print(entity)
        line = entity.split(':')
        params = line[1].split(",")
        contents = advogato_data_KG_source('source', params[0], int(params[1]))
        print(contents)
        with open("static/data/entity_relationships.json", 'w') as data:
            json.dump(contents, data)
        # name = {"entity":entity, "level":params[1]}
        name = {}
        name['entity'] = str(params[0])
        name['level'] = str(params[1])
        print(name)
        return render_template('entity_relationships.html', contents=name)
    elif "mention:" in entity:
        print(entity)
        line = entity.strip().split(":")
        mention = line[1]
        contents = mention2entity(mention)
        print(contents)
        with open("static/data/entity_mention.json", 'w') as data:
            json.dump(contents, data)
        urls = {}
        urls['mention'] = mention
        return render_template('entity_mention.html', contents=urls)
    elif "ad_trust:" in entity:
        print(entity)
        line = entity.strip().split(":")
        entities = line[1].split(",")
        source = entities[0]
        target = entities[1]
        cutoff = entities[2]
        print(source, target, cutoff)
        contents = get_paths(source, target, cutoff,'')
        with open("static/data/entity_entity_paths.json", 'w') as data:
            json.dump(contents, data)
        paths = {}
        paths['source'] = str(source)
        paths['target'] = str(target)
        paths['cutoff'] = str(cutoff)
        print(contents)
        if int(cutoff) == 1:
            paths['trust'] = get_trust_value_1(source, target)
        elif len(contents['links']) == 0:
            paths['trust'] = 0.0
        else:
            paths['trust'] = get_trust_value(source, target, cutoff)
        print(paths)
        return render_template('entity_entity_paths.html', contents=paths)
    elif "nlp:" in entity:
        print(entity)
        line = entity.strip().split(":")
        statement = line[1]
        contents = lexer(statement)
        with open("static/data/nlp.json", 'w') as data:
            json.dump(contents, data)
        return render_template('nlp.html')
    elif 'emotion' in entity:
        print(entity)
        line = entity.strip().split(":")
        statement = line[1]
        mydata = emotion(statement)
        return render_template('sentiment.html', contents=mydata)
    elif 'weibo' in entity:
        line = entity.strip().split(":")
        username = line[1]
        print("username:",username)
        user_id = get_weibo_userid(username)
        print(user_id)
        if user_id is None:
            user_id = get_weibo_userid_special(username)
        print("user_id:", user_id)
        if user_id == None:
            return "请确保输入的用户名正确无误~"
        contents, username = generate_weibo_user_graph(user_id=int(user_id))
        print(user_id)
        if contents == '':
            return "抱歉，因你过于帅气，我自己都凌乱了。"
        with open("static/data/weibo.json", 'w') as data:
            json.dump(contents, data)
        mydata = {}
        mydata['user_id'] = user_id
        mydata['username'] = username
        return render_template('weibo_graph.html', contents=mydata)
    elif 'network' in entity:
        line = entity.strip().split(":")
        entity = line[1]
        if entity == "特朗普":
            entity = "唐纳德·特朗普"
        if entity == '李小勇':
            entity = '李小勇[北京邮电大学教授]'
        file_name = "entity_attribution_{}.json"
        file_path = "static/data/entity_attr/"+file_name.format(entity)
        result = os.path.exists(file_path)
        baidu = {}
        baike_url = get_baike_url(entity)  # 百度百科的url
        baidu['url'] = baike_url
        baidu['entity'] = entity
        baidu['url'] = "http://47.105.58.24:8989/" + "static/data/links/" + file_name.format(entity)
        if result:
            print("已经有这个文件了")
            return render_template('entity_attribution.html', contents=baidu)
        contents, baike_url_2 = KG_View_2(entity)
        if '李小勇' in entity:
            contents = generate_lxy_contents()
        if len(contents) == 0:
            return "输入的实体暂不支持，请检查合法性后重新输入。"
        if entity == "唐纳德·特朗普":
            entity = "特朗普"
        related_urls = []
        #related_urls = get_related_urls(entity)
        if entity == "特朗普":
            entity = "唐纳德·特朗普"
        related_urls.append(baike_url)
        print("baike_url:",baike_url)
        with open("static/data/links/" + file_name.format(entity), 'w') as data:
            for url in related_urls:
                data.write(url+"\n")
        data.close()
        with open("static/data/entity_attr/"+file_name.format(entity), 'w') as data:
            json.dump(contents, data)
        return render_template('entity_attribution.html', contents=baidu)
    elif "fb_social" in entity:
        print(entity)
        line = entity.split(':')
        params = line[1].split(",")
        entity_id = params[0]
        entity_name = get_entity_name(entity_id)
        contents = advogato_data_KG_source('freebase', entity_name, int(params[1]))
        print(contents)
        with open("static/data/entity_relationships.json", 'w') as data:
            json.dump(contents, data)
        name = {}
        name['entity'] = str(entity_name)
        name['level'] = str(params[1])
        print(name)
        return render_template('entity_relationships.html', contents=name)
    elif "fb_relation" in entity:
        print(entity)
        line = entity.strip().split(":")
        entities = line[1].split(",")
        source = entities[0]
        target = entities[1]
        # cutoff = entities[2]
        print(source, target)
        contents = get_paths(source, target, 1, "freebase")
        infos = get_freebase_info(source, target)
        with open("static/data/entity_entity_paths.json", 'w') as data:
            json.dump(contents, data)
        paths = {}
        paths['source'] = str(source)
        paths['target'] = str(target)
        paths['cutoff'] = 1

        paths['trust'] = round(float32(infos.get('trust')), 3)
        paths['max_trust'] = infos.get('max_trust_relation')

        #paths['trust'] = round(float(infos.get('trust','0')), 3)
        #paths['max_trust'] = infos.get('max_trust_relation','')
        print(paths)
        return render_template('freebase_relation_trust.html', contents=paths)
    else:
        return "输入格式不合法，请检查后重新输入"

@app.route('/search')
def show_search():
    return render_template('search.html')

@app.route('/answer')
def question():
    # print("请求方式为:", request.method)
    # question = request.args.to_dict().get('question', '')
    # if question == '':
    #     return "你可能忘记提问了, 试试/answer?question=刘德华的妻子是谁"
    # print(question)
    # answer = question2info(question)
    # print(answer)
    # return json.dumps(answer, ensure_ascii=False)
    return render_template("robot.html")

@app.route('/mention')
def mention():
    print("请求方式为:", request.method)
    mention = request.args.to_dict().get('mention', '')
    if mention == '':
        return "你可能忘记提问了, 试试/mention?mention=泡泡糖"
    print(mention)
    answers = mention2entity(mention)
    print(answers)
    return json.dumps(answers, ensure_ascii=False)


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)
