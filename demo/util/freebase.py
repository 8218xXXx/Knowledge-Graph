# encoding=utf8

from util.data_model import init, execute
import os

path = os.getcwd()

def load_into_mysql(file=path+"/freebase/test.txt", sp='\t'):
    with open(file,'r') as data:
        lines = data.readlines()
        cnt = 0
        conn, cursor = init()  #初始化mysql
        sql = 'insert into freebase (source_entity, target_entity, relation) values ("{}","{}","{}")'
        for line in lines:
            contents = line.split(sp)
            source = contents[0]
            target = contents[1]
            relation = contents[2]
            print(source, target, relation)
            cnt = cnt+1
            execute(cursor,conn,sql.format(source,target,relation))
            print(sql.format(source,target,relation))
        print(cnt)

def load_entity2id_into_mysql(file=path+"/freebase/entity2id.txt", sp='\t'):
    with open(file,'r') as data:
        lines = data.readlines()
        cnt = 0
        conn, cursor = init()  #初始化mysql
        sql = 'insert into freebase_entity_id (entity_name, entity_id) values ("{}","{}")'
        for line in lines:
            contents = line.split(sp)
            entity_name = contents[0]
            entity_id = contents[1]
            print(entity_name, entity_id)
            cnt = cnt+1
            execute(cursor,conn,sql.format(entity_name,entity_id))
            print(sql.format(entity_name,entity_id))
        print(cnt)


def get_entity_name(entity_id):
    sql = "select * from freebase_entity_id where entity_id="+entity_id
    conn, cursor = init()  # 初始化mysql
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        return ""
    return result[0][1]

def get_freebase_info(source, target):
    source_name = get_entity_name(source)
    target_name = get_entity_name(target)
    sql_template = "select * from freebase where source_entity='{}' and target_entity='{}'"
    conn, cursor = init()  # 初始化mysql
    print(sql_template.format(source_name,target_name))
    cursor.execute(sql_template.format(source_name,target_name))
    result = cursor.fetchall()
    if len(result) == 0:
        print("hahahahha")
        return {}
    infos = {}
    content = tuple(result[0])
    print("content:",content)
    infos['rank'] = content[4]
    infos['trust'] = content[5]
    infos['max_trust_relation'] = content[6]
    print(infos)
    return infos

def test():
    file = "testRelationRaw.txt"
    cnt = 1
    sql_template = 'update freebase set rank_value="{}", trsut="{}", max_trust_relation="{}" where id={}'
    conn, cursor = init()
    with open(file, 'r') as data:
        lines = data.readlines()
        print(len(lines))
        for line in lines:
            contents = line.split('\t')
            triplet = contents[0]
            real_relation = contents[1]
            max_trust_relation = contents[2]
            rank = contents[3]
            trust = contents[4]
            print(triplet)
            print(real_relation)
            print(max_trust_relation)
            print(rank)
            print(trust)
            sql = sql_template.format(rank, str(1 - float(trust)), max_trust_relation, cnt)
            print(sql)
            cursor.execute(sql)
            conn.commit()
            cnt += 1
    print(cnt)

if __name__ == '__main__':
    # load_entity2id_into_mysql()
    load_into_mysql()


