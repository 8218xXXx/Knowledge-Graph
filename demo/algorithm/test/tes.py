from util.data_model import init, execute

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
            sql = sql_template.format(rank,str(1-float(trust)), max_trust_relation, cnt)
            print(sql)
            cursor.execute(sql)
            conn.commit()
            cnt+=1
    print(cnt)
