from util.data_model import init, execute
from settings import sql_template
def load_data_into_mysql():
	fname = "advogato"
	cnt = 0
	content = "source = {}, target = {}, and relation = {}"
	conn, cursor = init()
	with open(fname, 'r') as file:
		for line in file:
			line = line.strip()
			combo = line.split(" ")
			source = combo[0]
			target = combo[1]
			relation = combo[2]
			if source == target:
				continue
			print(content.format(source, target, relation))
			sql = sql_template.format(source, target, relation)
			execute(cursor, conn, sql)
			cnt += 1
	print(cnt)

if __name__ == '__main__':
    load_data_into_mysql()