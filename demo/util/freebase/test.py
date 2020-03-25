# encoding=utf8

from util.data_model import init, execute
import os

path = os.getcwd()



if __name__ == '__main__':
    file = path+"/entity2id.txt"
    load_into_mysql(file)

