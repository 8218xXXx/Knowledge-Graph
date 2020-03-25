# -*- coding: utf-8 -*-
import pymysql
import networkx as nx
from settings import max_nodes, mysql_password

def init():
	conn = pymysql.connect(
			host = 'localhost',
			port = 3306,
			user = 'root',
			password = mysql_password,
			charset ='utf8',
			db = 'online_social_networks')
	cursor = conn.cursor()
	return conn, cursor

def execute(cursor, conn, sql):
	try:
		cursor.execute(sql)
		conn.commit()
	except:
		print("存入数据库失败")
		conn.rollback()
	# 向数据库提交执行的语句

def get_all_user():
	fname = "advogato"
	users = set()
	with open(fname, 'r') as file:
		for line in file:
			line = line.strip()
			combo = line.split(" ")
			source = combo[0]
			target = combo[1]
			users.add(source)
			users.add(target)
	print(len(users))
	print(users)


def paths(source, target, cutoff=4, kind=''):
	if kind == 'freebase':
		source_sql = 'select * from freebase_entity_id where entity_id='+source
		target_sql = 'select * from freebase_entity_id where entity_id=' + target
		conn, cursor = init()
		cursor.execute(source_sql)
		result = cursor.fetchall()
		source = result[0][1]
		cursor.execute(target_sql)
		result = cursor.fetchall()
		target = result[0][1]
		fname = "train.txt"
		sp = '\t'
	else:
		fname = "advogato"
		sp = ' '
	edges = []
	with open(fname, 'r') as file:
		for line in file:
			line = line.strip()
			combo = line.split(sp)
			source_1 = combo[0]
			target_1 = combo[1]
			relation = combo[2]
			if source_1 == target_1:
				continue
			edges.append((source_1, target_1, relation))
	print(source)
	G = nx.DiGraph()
	G.add_weighted_edges_from(edges)
	print(G.number_of_edges())           # 产生了一个社交图
	paths = list(nx.all_simple_paths(G,source,target, cutoff=int(cutoff)))
	print(len(paths))

	contents = {}
	contents["type"] = "force"  # 属性 type
	categories = []
	no_repeat_categories = ['源节点', '目标节点', '中间节点']
	categories_to_int = {}
	categories_to_int['源节点'] = 0
	categories_to_int['目标节点'] = 1
	categories_to_int['中间节点'] = 2
	cnt = 0
	for category in no_repeat_categories:
		node = {'name': category, 'keyword': {}, 'base': category}
		categories.append(node)
		cnt += 1
	contents['categories'] = categories  # 属性 categories
	# node = {'name': avp[1], 'value': str(avp[1]), 'category': categories_to_int[avp[0]]}
	# link = {'source': 0, 'target': cnt + 1, 'value': avp[0]}
	no_repeat_nodes = set()
	if len(paths) > max_nodes:
		for i in range(0,max_nodes):
			print(paths[i])
			for j in range(0, len(paths[i])-1):
				current_source = paths[i][j]                # 源点
				current_target = paths[i][j+1]				# 目标点
				no_repeat_nodes.add(current_source)
				no_repeat_nodes.add(current_target)
	else:
		print(paths)
		for i in range(0,len(paths)):
			for j in range(0, len(paths[i])-1):
				current_source = paths[i][j]
				current_target = paths[i][j+1]
				no_repeat_nodes.add(current_source)
				no_repeat_nodes.add(current_target)
	no_repeat_nodes = list(no_repeat_nodes)
	print("no_repeat_nodes", no_repeat_nodes)
	nodes = []
	for node in no_repeat_nodes:
		if node == source:
			category = "源节点"
		elif node == target:
			category = "目标节点"
		else:
			category = "中间节点"
		node = {'name': node, 'value': str(node), 'category': categories_to_int[category]}
		nodes.append(node)
	links = []

	if len(paths) > max_nodes:
		for i in range(0,max_nodes):
			print(paths[i])
			for j in range(0, len(paths[i])-1):
				current_source = paths[i][j]                # 源点
				current_target = paths[i][j+1]				# 目标点
				relation = G.get_edge_data(current_source, current_target)   # 关系
				# if current_source == source:
				# 	relation = "source"
				# if current_source == target:
				# 	relation = "target"
				link = {'source': no_repeat_nodes.index(current_source), 'target': no_repeat_nodes.index(current_target), 'value':relation['weight']}
				links.append(link)
				print(links)
	else:
		print(paths)
		for i in range(0,len(paths)):
			for j in range(0, len(paths[i])-1):
				current_source = paths[i][j]  # 源点
				current_target = paths[i][j + 1]  # 目标点
				relation = G.get_edge_data(current_source, current_target)  # 关系
				# if current_source == source:
				# 	relation = "source"
				# if current_source == target:
				# 	relation = "target"
				link = {'source': no_repeat_nodes.index(current_source),'target': no_repeat_nodes.index(current_target), 'value': relation['weight']}
				links.append(link)
				# print(links)
	contents['nodes'] = nodes
	contents['links'] = links
	print("links:", links)
	print("nodes:", nodes)
	return contents


if __name__ == '__main__':
	nodes = [1,2,3]
	if 4 not in nodes:
		print(nodes)