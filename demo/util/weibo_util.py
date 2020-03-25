# encoding=utf8
import requests
from util.data_model import init
from util.weibo import get_weibo_userid, main, get_weibo_userid_special
from settings import follows_limit, weibo_contents_limit


user_profile_template = '''
    select * from weibo_user_profile where user_id={}
'''

user_profile_2_template = '''
    select * from weibo_user_profile_2 where user_id={}
'''

user_follow_template = '''
    select * from weibo_follow_user where user_id={}
'''

weibo_contents_template = '''
    select * from weibo_user_content where user_id={}
'''
user_profile_info = '''
    username={}, user_id={}, weibo_num={}, following={}, follower={}
'''
def get_weibo_user_profile(user_id=''):
    if user_id == '':
        return {'message':'请输入user_id'}
    conn, cursor = init()
    cursor.execute(user_profile_template.format(user_id))
    results = cursor.fetchall()
    if len(results) == 1:
        results = results[0]
    info = user_profile_info.format(results[1], results[2],results[3],results[4],results[5],)
    return info

def get_weibo_user_follow(user_id=''):
    if user_id == '':
        return {'message':'请输入user_id'}
    conn, cursor = init()
    cursor.execute(user_follow_template.format(user_id))
    results = cursor.fetchall()
    if len(results) == 0:
        return {'message':'该用户关注的人为0'}
    for row in results:
        pass

def generate_weibo_user_graph(user_id=''):
    if user_id == '':
        return {'message':'请输入user_id'}
    contents = {}
    contents["type"] = "force"
    ##  类别
    categories = []
    no_repeat_categories = ['关注数量','粉丝','微博内容数量','原创微博','转发微博','微博发布地点',
                            '微博发布时间','微博点赞数','微博转发数','微博评论数','微博发布工具',
                            '关注','微博检索用户','家乡','简介','认证信息','教育背景','标签','性别']
    category_to_int = {
        '关注数量':0, '粉丝':1,
        '微博内容数量':2, '原创微博':3,
        '转发微博':4, '微博发布地点':5,
        '微博发布时间':6, '微博点赞数':7,
        '微博转发数':8, '微博评论数':9,
        '微博发布工具':10, '关注':11,
        '微博检索用户':12, '家乡':13,'简介':14,'认证信息':15,'教育背景':16,'标签':17,'性别':18
    }
    for category in no_repeat_categories:
        node = {'name': category, 'keyword': {}, 'base': category}
        categories.append(node)
    contents["categories"] = categories

    node_name_value={}

    ### 节点nodes
    nodes = []
    links = []
    real_nodes = []
    ##  user profile
    conn, cursor = init()
    cursor.execute(user_profile_template.format(user_id))
    profile = cursor.fetchall()
    if len(profile) == 0:
        return "", ""
    if len(profile) >= 1:
        profile = profile[0]

    node = {'name':profile[1], 'value':profile[1], 'category':category_to_int['微博检索用户']}
    nodes.append(node)

    real_nodes.append(profile[1])
    node_name_value[profile[1]] = profile[1]

    node_name_value['微博内容数量'] = profile[3]
    node = {'name': '微博内容数量', 'value': profile[3], 'category': category_to_int['微博内容数量']}
    nodes.append(node)

    node_name_value['关注数量'] = profile[4]
    node = {'name': '关注数量', 'value': profile[4], 'category': category_to_int['关注数量']}
    nodes.append(node)

    node_name_value['粉丝'] = profile[5]
    node = {'name': '粉丝', 'value': profile[5], 'category': category_to_int['粉丝']}
    nodes.append(node)
    real_nodes.append('微博内容数量')
    real_nodes.append('关注数量')
    real_nodes.append('粉丝')

    cursor.execute(user_profile_2_template.format(user_id))
    profile = cursor.fetchall()
    if len(profile) == 0:
        return "",""
    else:
        profile = profile[0]
    print(profile)
    if profile[4].strip() != "":
        node_name_value['认证信息'] = profile[4]
        node = {'name': '认证信息', 'value': profile[4], 'category': category_to_int['认证信息']}
        nodes.append(node)
        real_nodes.append('认证信息')
        link = {'source': real_nodes.index(profile[1]), 'target': real_nodes.index('认证信息'),
                'value': node_name_value['认证信息']}
        links.append(link)
    if profile[5].strip() != "":
        node_name_value['家乡'] = profile[5]
        node = {'name': '家乡', 'value': profile[5], 'category': category_to_int['家乡']}
        nodes.append(node)
        real_nodes.append('家乡')
        link = {'source': real_nodes.index(profile[1]), 'target': real_nodes.index('家乡'),
                'value': node_name_value['家乡']}
        links.append(link)
    if profile[7].strip() != "":
        node_name_value['简介'] = profile[7]
        node = {'name': '简介', 'value': profile[7], 'category': category_to_int['简介']}
        nodes.append(node)
        real_nodes.append('简介')
        link = {'source': real_nodes.index(profile[1]), 'target': real_nodes.index('简介'),
                'value': node_name_value['简介']}
        links.append(link)
    if profile[10].strip() != "":
        node_name_value['教育背景'] = profile[10]
        node = {'name': '教育背景', 'value': profile[10], 'category': category_to_int['教育背景']}
        nodes.append(node)
        real_nodes.append('教育背景')
        link = {'source': real_nodes.index(profile[1]), 'target': real_nodes.index('教育背景'),
                'value': node_name_value['教育背景']}
        links.append(link)
    if profile[8].strip() != "":
        node_name_value['标签'] = profile[8]
        node = {'name': '标签', 'value': profile[8], 'category': category_to_int['标签']}
        nodes.append(node)
        real_nodes.append('标签')
        link = {'source': real_nodes.index(profile[1]), 'target': real_nodes.index('标签'),
                'value': node_name_value['标签']}
        links.append(link)
    if profile[9].strip() != "":
        node_name_value['性别'] = profile[9]
        node = {'name': '性别', 'value': profile[9], 'category': category_to_int['性别']}
        nodes.append(node)
        real_nodes.append('性别')
        link = {'source': real_nodes.index(profile[1]), 'target': real_nodes.index('性别'),
                'value': node_name_value['性别']}
        links.append(link)

    link = {'source': real_nodes.index(profile[1]), 'target': real_nodes.index('关注数量'), 'value': node_name_value['关注数量']}
    links.append(link)

    link = {'source': real_nodes.index(profile[1]), 'target': real_nodes.index('粉丝'),
            'value': node_name_value['粉丝']}
    links.append(link)

    link = {'source': real_nodes.index(profile[1]), 'target': real_nodes.index('微博内容数量'),
            'value': node_name_value['微博内容数量']}
    links.append(link)

    # user follow
    cursor.execute(user_follow_template.format(user_id))
    follows = cursor.fetchall()
    if len(follows) > follows_limit:
        follows = follows[:follows_limit]
    for follow in follows:
        follow_name = follow[3]
        follow_link = follow[4]
        node_name_value[follow_name] = follow_link
        node = {'name': follow_name, 'value': follow_link, 'category': category_to_int['关注']}
        nodes.append(node)
        real_nodes.append(follow_name)
        link = {'source': real_nodes.index('关注数量'), 'target': real_nodes.index(follow_name),
                'value': node_name_value[follow_name]}
        links.append(link)
    # user contents
    cursor.execute(weibo_contents_template.format(user_id))
    weibo_contents = cursor.fetchall()
    if len(weibo_contents) > weibo_contents_limit:
        weibo_contents = weibo_contents[:weibo_contents_limit]
    cnt = 1
    for content in weibo_contents:
        text = content[3]
        postion = content[4]
        time = content[5]
        up = content[6]
        repost = content[7]
        comment = content[8]
        tool = content[9]
        real_nodes.append('微博内容'+ str(cnt))
        node_name_value['微博内容'+ str(cnt)] = text
        if '转发理由' in text:
            cate = '转发微博'
        else:
            cate = '原创微博'
        node = {'name': '微博内容'+ str(cnt), 'value': text, 'category': category_to_int[cate]}
        nodes.append(node)
        link = {'source': real_nodes.index('微博内容数量'), 'target': real_nodes.index('微博内容'+ str(cnt)),
                'value': node_name_value['微博内容'+ str(cnt)]}
        links.append(link)

        real_nodes.append('微博发布地点'+ str(cnt))
        node_name_value['微博发布地点'+ str(cnt)] = postion
        node = {'name': '微博发布地点'+ str(cnt), 'value': postion, 'category': category_to_int['微博发布地点']}
        nodes.append(node)
        link = {'source': real_nodes.index('微博内容'+ str(cnt)), 'target': real_nodes.index('微博发布地点'+ str(cnt)),
                'value':postion}
        links.append(link)

        real_nodes.append('微博发布时间'+ str(cnt))
        node_name_value['微博发布时间'+ str(cnt)] = time
        node = {'name': '微博发布时间'+ str(cnt), 'value': time, 'category': category_to_int['微博发布时间']}
        nodes.append(node)
        link = {'source': real_nodes.index('微博内容'+ str(cnt)), 'target': real_nodes.index('微博发布时间'+ str(cnt)),
                'value': time}
        links.append(link)

        real_nodes.append('微博点赞数'+ str(cnt))
        node_name_value['微博点赞数'+ str(cnt)] = up
        node = {'name': '微博点赞数'+ str(cnt), 'value': up, 'category': category_to_int['微博点赞数']}
        nodes.append(node)
        link = {'source': real_nodes.index('微博内容'+ str(cnt)), 'target': real_nodes.index('微博点赞数'+ str(cnt)),
                'value': up}
        links.append(link)

        real_nodes.append('微博转发数'+ str(cnt))
        node_name_value['微博转发数'+ str(cnt)] = repost
        node = {'name': '微博转发数'+ str(cnt), 'value': repost, 'category': category_to_int['微博转发数']}
        nodes.append(node)
        link = {'source': real_nodes.index('微博内容'+ str(cnt)), 'target': real_nodes.index('微博转发数'+ str(cnt)),
                'value': repost}
        links.append(link)

        real_nodes.append('微博评论数'+ str(cnt))
        node_name_value['微博评论数'+ str(cnt)] = comment
        node = {'name': '微博评论数'+ str(cnt), 'value': comment, 'category': category_to_int['微博评论数']}
        nodes.append(node)
        link = {'source': real_nodes.index('微博内容'+ str(cnt)), 'target': real_nodes.index('微博评论数'+ str(cnt)),
                'value': comment}
        links.append(link)

        real_nodes.append('微博发布工具'+ str(cnt))
        node_name_value['微博发布工具'+ str(cnt)] = tool
        node = {'name': '微博发布工具'+ str(cnt), 'value': tool, 'category': category_to_int['微博发布工具']}
        nodes.append(node)
        link = {'source': real_nodes.index('微博内容'+ str(cnt)), 'target': real_nodes.index('微博发布工具'+ str(cnt)),
                'value': tool}
        links.append(link)
        cnt += 1

    contents['nodes'] = nodes
    contents['links'] = links

    return contents, profile[1]


def get_userid(username=''):
    user_id = get_weibo_userid(username)
    return user_id

def save_weibo_info(user_id):
    main(user_id)

if __name__ == '__main__':
    result = get_weibo_user_profile(user_id='1729370543')
    print(result)
    get_weibo_user_follow(user_id='1729370543')
