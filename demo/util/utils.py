# encoding=utf8
import requests
from util.data_model import init, paths
from settings import max_nodes_per_level, source_template, target_template, entity_url, mention_url, info_url, \
    level_to_int, relationship_list
from util.baidu import get_baike_url
import networkx as nx
from PIL import Image
import json
import random
import os
import numpy as np


def generate_lxy_contents(is_mention=False):
    entity = '李小勇[北京邮电大学教授]'
    contents = {}
    contents["type"] = "force"  # 属性 type
    categories = []
    no_repeat_categories = ['中文名','职业','国籍','学位/学历','民族','专业方向','出生日期','职务','曾任职','毕业院校']
    categories_to_int = {}
    cnt = 0
    for category in no_repeat_categories:
        node = {'name': category, 'keyword': {}, 'base': category}
        categories.append(node)
        categories_to_int[category] = cnt
        cnt += 1
    node = {'name': '检索实体', 'keyword': {}, 'base': '检索实体'}
    print(categories_to_int)
    categories.append(node)
    categories_to_int['检索实体'] = cnt
    contents['categories'] = categories  # 属性 categories
    nodes = []
    links = []
    node = {'name': entity, 'value': entity, 'category': categories_to_int['检索实体']}
    nodes.append(node)
    cnt = 0
    knowledge = [['中文名','李小勇'],['职业','教师'],['国籍','中国'],['学位/学历','博士'],['民族','汉族'],['专业方向','分布式计算与可信服务'],
                 ['出生日期','1975年'],['职务','北京邮电大学网络空间安全学院副院长'],['曾任职','北京邮电大学软件学院副院长'],['毕业院校','西安交通大学']]
    for avp in knowledge:
        node = {'name': avp[1], 'value': str(avp[1]), 'category': categories_to_int[avp[0]]}
        link = {'source': 0, 'target': cnt + 1, 'value': avp[0]}
        nodes.append(node)
        links.append(link)
        cnt += 1
        if is_mention == True:
            continue
        if str(avp[0]) in relationship_list:
            print("-----------\n")
            print(avp[0])
            current_cnt = cnt
            url = entity_url.format(avp[1])
            sess = requests.get(url)  # 请求
            text = sess.text  # 获取返回的数据
            response = eval(text)  # 转为字典类型
            if response['message'] is "error":
                continue
            knowledge_2 = response['data']
            for avp_2 in knowledge_2['avp']:
                node = {'name': avp_2[1], 'value': str(avp_2[1]), 'category': 0}
                link = {'source': current_cnt, 'target': cnt + 1, 'value': avp_2[0]}
                nodes.append(node)
                links.append(link)
                cnt += 1
    contents['nodes'] = nodes
    contents['links'] = links
    return contents

def get_trust_value_1(source, target):
    file_path = os.getcwd() + "/static/data/advogato"
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            contents = line.strip().split(' ')
            one = contents[0]
            two = contents[1]
            relation = contents[2]
            if one == str(source) and two == str(target):
                return level_to_int[relation]

def Normalize(data):
    m = np.mean(data)
    mx = max(data)
    mn = min(data)
    return [(float(i) - m) / (mx - mn) for i in data]


def get_trust_value(source, target, cutoff):
    file_path = os.getcwd() + "/static/data/page_rank.txt"
    print(file_path)
    flag = 0
    trust = 0
    trust_vector = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            contents = line.split(',')
            name = contents[0]
            value = contents[1]
            if flag == 2:
                break
            if name == str(source):
                flag+=1
                trust += float(value)
                trust_vector.append(float(value))
                print(value)
            if name == str(target):
                flag+=1
                trust += float(value)
                trust_vector.append(float(value))
                print(value)
    trust_vector.append((3-float(cutoff))*(3-float(cutoff)))
    trust = np.linalg.norm(trust_vector)
    if trust > 1:
        return round(1 / trust,2)
    return round(trust, 2)

def KG_View_lxy():
    source_node = '李小勇[北京邮电大学教授]'
    knowledge = [['中文名', '李小勇'], ['职业', '教师'], ['国籍', '中国'], ['学位/学历', '博士'], ['民族', '汉族'], ['专业方向', '分布式计算与可信服务'],
                 ['出生日期', '1975年'], ['职务', '北京邮电大学网络空间安全学院副院长'], ['曾任职', '北京邮电大学软件学院副院长'], ['毕业院校', '西安交通大学']]
    nodes = []
    for avp in knowledge:
        # if source_node in avp[1]:
        #     continue
        node = {'source': source_node, 'target': avp[1], 'type': "resolved", 'rela': avp[0]}
        nodes.append(node)
    links = []
    for i in range(len(nodes)):
        node = nodes[i]
        links.append(node)
    print(links)
    nodes = []
    nodes.append(links)
    nodes.append(source_node)
    return nodes

def KG_View(entity):
    url = entity_url.format(entity)
    sess = requests.get(url)  # 请求
    text = sess.text  # 获取返回的数据
    response = eval(text)  # 转为字典类型
    knowledge = response['data']
    nodes = []
    if len(knowledge) == 0:
        return []
    source_node = knowledge['entity']
    for avp in knowledge['avp']:
        if avp[1] == knowledge['entity']:
            continue
        node = {'source': source_node, 'target': avp[1], 'type': "resolved", 'rela': avp[0]}
        nodes.append(node)
    links = []
    for i in range(len(nodes)):
        node = nodes[i]
        links.append(node)
    print(links)
    nodes = []
    nodes.append(links)
    nodes.append(source_node)
    return nodes

def KG_View_2(entity):
    print("KG_View-----------")
    url = entity_url.format(entity)
    sess = requests.get(url)  # 请求
    text = sess.text  # 获取返回的数据
    response = eval(text)  # 转为字典类型
    if response['message'] is "error":
        print("hahaha")
        return [],""
    knowledge = response['data']
    if len(knowledge) == 0:
        return [],""
    baike_url = get_baike_url(knowledge['entity'])  # 百度百科的url
    contents = {}
    contents["type"] = "force"                  # 属性 type
    categories = []
    no_repeat_categories = set()
    print(knowledge['avp'])
    if knowledge['entity'] == '习近平':
        print()
        temp = ['妻子','彭丽媛']
        knowledge['avp'].append(temp)
        print(type(knowledge['avp']))
    for avp in knowledge['avp']:
        category = avp[0]
        no_repeat_categories.add(category)
    no_repeat_categories = list(no_repeat_categories)   #  类型确定
    categories_to_int = {}
    cnt = 0
    for category in no_repeat_categories:
        node = {'name': category, 'keyword': {}, 'base': category}
        categories.append(node)
        categories_to_int[category] = cnt
        cnt += 1
    node = {'name': '检索实体', 'keyword': {}, 'base': '检索实体'}
    print(categories_to_int)
    categories.append(node)
    categories_to_int['检索实体'] = cnt
    contents['categories'] = categories           # 属性 categories
    nodes = []
    links = []
    node = {'name': entity, 'value': entity, 'category': categories_to_int['检索实体']}
    nodes.append(node)
    cnt = 0
    for avp in knowledge['avp']:
        node = {'name': avp[1], 'value': str(avp[1]), 'category': categories_to_int[avp[0]]}
        link = {'source': 0, 'target': cnt + 1, 'value': avp[0]}
        nodes.append(node)
        links.append(link)
        cnt += 1
        if str(avp[0]) in relationship_list:
            print("-----------\n")
            print(avp[0])
            current_cnt = cnt
            url = entity_url.format(avp[1])
            sess = requests.get(url)  # 请求
            text = sess.text  # 获取返回的数据
            response = eval(text)  # 转为字典类型
            if response['message'] is "error":
                continue
            knowledge_2 = response['data']
            for avp_2 in knowledge_2['avp']:
                node = {'name': avp_2[1], 'value': str(avp_2[1]), 'category': 0}
                link = {'source': current_cnt, 'target': cnt + 1, 'value': avp_2[0]}
                nodes.append(node)
                links.append(link)
                cnt += 1
    contents['nodes'] = nodes
    contents['links'] = links
    return contents, baike_url

def advogato_data_KG_source(kind, entity, level):
    source_sql = source_template
    if kind == 'freebase':
        source_sql = "select * from freebase where source_entity='{}'"
    conn, cursor = init()
    sql = source_sql.format(entity)
    entity01 = {}
    cursor.execute(sql)
    results = cursor.fetchall()
    per_level_nodes = 0
    contents = {}
    contents["type"] = "force"  # 属性 type
    no_repeat_categories = ['指定实体', '关联实体']
    category_to_int = {"指定实体":0, "关联实体":1}
    print(len(results))
    print(no_repeat_categories)
    categories = []
    for category in no_repeat_categories:
        node = {'name': category, 'keyword': {}, 'base': category}
        categories.append(node)
    contents["categories"] = categories
    print(contents)
    nodes = []
    links = []
    real_nodes = []
    for row in results:
        source_node = row[1]
        target_node = row[2]
        entity01[source_node] = 1  # 表示已经查询过了
        entity01[target_node] = 0  # 表示还未查询
        if row[1] not in real_nodes:
            real_nodes.append(row[1])
            if row[1] == entity:
                category = "指定实体"
            else:
                category = "关联实体"
            node = {'name': row[1], 'value': str(row[1]), 'category': category_to_int[category]}
            nodes.append(node)
        if row[2] not in real_nodes:
            real_nodes.append(row[2])
            if row[2] == entity:
                category = "指定实体"
            else:
                category = "关联实体"
            node = {'name': row[2], 'value': str(row[2]), 'category': category_to_int[category]}
            nodes.append(node)
        link = {'source': real_nodes.index(row[1]), 'target': real_nodes.index(row[2]), 'value': row[3]}
        links.append(link)
        per_level_nodes += 1
        if per_level_nodes > max_nodes_per_level:
            break
    helper(entity01, nodes, level - 1, conn, cursor, links, category_to_int, real_nodes, source_template)
    contents['nodes'] = list(nodes)
    contents['links'] = list(links)
    return contents


def helper(entity01, nodes, level, conn, cursor, links, category_to_int,real_nodes, source_template):
    if level <= 0:
        return
    per_level_nodes = 0
    for entity in list(entity01.keys()):
        print(entity)
        used = entity01[entity]
        if used == 1:
            continue
        sql = source_template.format(entity)
        cursor.execute(sql)
        results = cursor.fetchall()

        for row in results:
            source_node = row[1]
            target_node = row[2]
            entity01[source_node] = 1  # 表示已经查询过了
            entity01[target_node] = 0  # 表示还未查询
            if source_node not in real_nodes:
                real_nodes.append(source_node)
                node = {'name': source_node, 'value': str(source_node), 'category': category_to_int['关联实体']}
                nodes.append(node)
            if target_node not in real_nodes:
                real_nodes.append(target_node)
                node = {'name': target_node, 'value': str(target_node), 'category': category_to_int['关联实体']}
                nodes.append(node)
            link = {'source': real_nodes.index(source_node), 'target': real_nodes.index(target_node), 'value': row[3]}
            links.append(link)
            per_level_nodes += 1
            if per_level_nodes > max_nodes_per_level:
                break
    helper(entity01, nodes, level - 1, conn, cursor, links, category_to_int, real_nodes,source_template)


def advogato_data_KG_target(kind, entity):
    '''
    这个暂时没什么用
    :param kind:
    :param entity:
    :return:
    '''
    conn, cursor = init()
    if kind == 'source':
        sql = source_template.format(entity)
    else:
        sql = target_template.format(entity)
    cursor.execute(sql)
    results = cursor.fetchall()
    print(len(results))
    nodes = []  # 最终结果
    seconds = []
    cnt = 0
    for row in results:
        node = {'source': row[1], 'target': row[2], 'type': "resolved", 'rela': row[3]}
        nodes.append(node)
        seconds.append(row[2])
        cnt += 1
        if cnt > max_nodes_per_level:
            break
    thirds = []
    cnt = 0
    for source in seconds:
        sql = source_template.format(source)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            node = {'source': row[1], 'target': row[2], 'type': "resolved", 'rela': row[3]}
            nodes.append(node)
            thirds.append(row[2])
            cnt += 1
            if cnt > max_nodes_per_level:
                break
    cnt = 0
    for source in thirds:
        sql = source_template.format(source)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            node = {'source': row[1], 'target': row[2], 'type': "resolved", 'rela': row[3]}
            nodes.append(node)
            cnt += 1
            if cnt > max_nodes_per_level:
                break
    print(nodes)

    return nodes


def mention2entity(mention):
    '''
    获取歧义关系
    :param mention:
    :return:
    '''
    if mention == "习大大":
        nodes = []
        node = {'source': mention, 'target': "习近平", 'type': "resolved", 'rela': '同名'}
        nodes.append(node)
        second_nodes = KG_View("习近平")
        for node in second_nodes[0]:
            nodes.append(node)
        return nodes
    else:
        url = mention_url.format(mention)
        sess = requests.get(url)
        text = sess.text
        entities = eval(text)  # 转为字典类型
        print(entities)
        print(entities['data'])
        contents = {}
        contents['type'] = 'force'
        no_repeat_categories = ["歧义实体", "同名实体", "属性"]
        category_to_int = {"歧义实体": 0, "同名实体": 1, "属性":2}
        categories = []
        for cate in no_repeat_categories:
            node = {'name': cate, 'keyword': {}, 'base': cate}
            categories.append(node)
        contents['categories'] = categories

        real_nodes = []
        nodes = []
        real_nodes.append(mention)
        node = {'name': mention, 'value': str(mention), 'category': category_to_int['歧义实体']}
        nodes.append(node)
        links = []
        for row in entities['data']:
            print("row[0]:", row[0])
            if row[0] == '李小勇[北京邮电大学教授]':
                ccurrent_contents = KG_View_lxy()
            else:
                ccurrent_contents = KG_View(row[0])
            if len(ccurrent_contents) == 0:
                if row[0] not in real_nodes:
                    real_nodes.append(row[0])
                    node = {'name':row[0], 'value':str(row[0]), 'category':category_to_int['同名实体']}
                    nodes.append(node)
                link = {'source': real_nodes.index(mention), 'target': real_nodes.index(row[0]), 'value': '同名'}
                links.append(link)
                continue
            print(ccurrent_contents)
            second_nodes = ccurrent_contents[0]
            source_node = ccurrent_contents[1]
            if source_node not in real_nodes:
                real_nodes.append(source_node)
                node = {'name':source_node, 'value':str(source_node), 'category':category_to_int['同名实体']}
                nodes.append(node)
            link = {'source': real_nodes.index(mention), 'target': real_nodes.index(source_node), 'value': '同名'}
            links.append(link)
            for node in second_nodes:
                if node['source'] not in real_nodes:
                    real_nodes.append(node['source'])
                    current_node = {'name': node['source'], 'value': str(node['source']), 'category': category_to_int['属性']}
                    nodes.append(current_node)
                if node['target'] not in real_nodes:
                    real_nodes.append(node['target'])
                    current_node = {'name': node['target'], 'value': str(node['target']), 'category': category_to_int['属性']}
                    nodes.append(current_node)
                print("-----------------------------")
                print(real_nodes)
                print("------------------------------")
                print(node)
                link = {'source': real_nodes.index(node['source']), 'target': real_nodes.index(node['target']), 'value': node['rela']}
                links.append(link)
        contents['nodes'] = nodes
        contents['links'] = links
    return contents


def question2info(question):
    '''
    问答
    :param questtion:
    :return:
    '''
    url = info_url.format(question)
    sess = requests.get(url)
    text = sess.text
    answer = eval(text)
    print(answer)
    return answer


def get_paths(source, target, cutoff, kind):
    return paths(source, target, cutoff, kind)


'''
    page_rank值
'''


def get_page_rank():
    fname = "advogato"
    edges = []
    with open(fname, 'r') as file:
        for line in file:
            line = line.strip()
            combo = line.split(" ")
            source_1 = combo[0]
            target_1 = combo[1]
            relation = level_to_int[combo[2]]
            if source_1 == target_1:
                continue
            edges.append((source_1, target_1, relation))
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    pr = nx.pagerank(G, alpha=0.9)
    print(pr)
    cnt = 0
    pairs = normalizatiion(pr)
    with open("page_rank.txt", 'w') as data:
        for name, value in pairs.items():
            content = name + "," + str(value)
            data.write(content + '\n')
    print(cnt)


def set_size_image():
    file = "logo.png"
    out_file = "out_logo.jpg"
    logo = Image.open(file)
    (x, y) = logo.size
    print(x, y)
    x1 = 50
    y1 = 50
    out = logo.resize((x1, y1), Image.ANTIALIAS)
    out.save(out_file, quality=95)


'''
    生成图
'''


def generate_graph():
    fname = "advogato"
    edges = []
    with open(fname, 'r') as file:
        for line in file:
            line = line.strip()
            combo = line.split(" ")
            source_1 = combo[0]
            target_1 = combo[1]
            relation = level_to_int[combo[2]]
            if source_1 == target_1:
                continue
            edges.append((source_1, target_1, relation))
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    return G


'''
    计算网络中数据的中心性指标
'''


def get_centrality():
    G = generate_graph()
    pairs = nx.degree_centrality(G)
    cnt = 0
    for name, value in pairs.items():
        cnt += 1
        print(name, value)
    print(cnt)
    pairs = normalizatiion(pairs)
    with open("centrality.txt", 'w') as data:
        for name, value in pairs.items():
            content = name + "," + str(value)
            data.write(content + '\n')


'''
eigenvector_centrality
'''


def get_eigenvector_centrality():
    G = generate_graph()
    pairs = nx.eigenvector_centrality(G)
    cnt = 0
    for name, value in pairs.items():
        cnt += 1
        print(name, value)
    print(cnt)
    pairs = normalizatiion(pairs)
    with open("eigenvector_centrality.txt", 'w') as data:
        for name, value in pairs.items():
            content = name + "," + str(value)
            data.write(content + '\n')


'''
    归一化
'''


def normalizatiion(pairs):
    min_value = 1000000
    max_value = -1000000
    for name, value in pairs.items():
        min_value = min(min_value, value)
        max_value = max(max_value, value)
    print(min_value, max_value)
    for name, value in pairs.items():
        value = (value - min_value) / (max_value - min_value)
        pairs.update({name: value})
    print(pairs)
    return pairs


def test():
    with open("page_rank_2.json", 'rb') as f:
        contents = json.load(f)
        nodes = contents['nodes']
        links = contents['links']
        cnt = 0
        for pair in nodes:
            if pair['name'] == "PositionErrorCallback":
                print(cnt)
                break
            cnt += 1


def generate_json_file():
    all_file = {}
    with open("page_rank_2.json", 'rb') as f:
        contents = json.load(f)
        type = contents['type']
        categories = contents['categories']
        print(type)
        print(categories)
        all_file["type"] = type
        all_file["categories"] = categories
    nodes = []
    name2int = {}
    cnt = 0
    with open("page_rank.txt", 'r') as data:
        for line in data:
            combo = line.strip().split(",")
            name = combo[0]
            value = combo[1]
            print(name, value)
            category = random.randint(0, 4)
            # print("category:",category)
            node = {'name': name, 'value': float(value)*10, 'category': category}
            name2int[name] = cnt
            if len(nodes) == 300:
                continue
            nodes.append(node)
            print(node)
            cnt += 1
    # print(nodes)
    all_file["nodes"] = nodes

    # print(name2int)
    links = []
    with open("advogato", 'r') as data:
        for line in data:
            combo = line.strip().split(" ")
            source = combo[0]
            target = combo[1]
            if source == target:
                continue
            # print(name2int[source], name2int[target])
            link = {
                       "source": name2int[source],
                       "target": name2int[target]
                   }
            links.append(link)
            if len(links) == 700:
                break
            # print(len(links))
    all_file["links"] = links

    # print(all_file)
    with open("test_json.json", 'w') as data:
        json.dump(all_file, data)


if __name__ == '__main__':
    # KG_View('习近平')
    # advogato_data_KG_target('raph', "1", 'miguel')
    # mention2entity('马云')
    # path_test()
    # question2info("美国总统是谁？")
    # get_page_rank()
    # set_size_image()
    # get_eigenvector_centrality()
    # generate_json_file()
    # print(random.randint(0,4))
    r = advogato_data_KG_source("source", 'miguel', 1)
    print(r)
