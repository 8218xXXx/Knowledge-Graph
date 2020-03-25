from semantic import Analysis

if __name__ == '__main__':
    text = "你是谁啊"
    slu = Analysis(text)
    data = slu.analysis()  # 解析
    print(data)  # 总的结果
    print('--------------------------')

    print("分词：",slu.cws)  # 分词

    print("词性标注",slu.pos)  # 词性标注

    print("命名实体识别",slu.ner)  # 命名实体识别

    print("领域分类",slu.domain)  # 领域分类

    print("意图识别",slu.intent)  # 意图识别

    print("槽填充",slu.slot)  # 槽填充