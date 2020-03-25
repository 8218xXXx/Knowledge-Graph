# encoding=utf8

import requests, json
host = "http://zhishi.me/api/entity/{}"

def get_related_urls(entity):
    print(host.format(entity))
    response = requests.get(host.format(entity)).content
    if response.decode("utf-8") == "not found":
        return []
    print(response)
    response = json.loads(response)
    print(response)
    if response.get('baidubaike', '') == '':
        contents = response['hudongbaike']
    else:
        contents = response.get('baidubaike', '')
    if contents == '':
        return []
    if contents.get("pageRedirects","") != "":
        print(contents.get("pageRedirects")[0])
        entity_link = str(contents.get("pageRedirects")[0])
        print(entity_link.split("resource/")[1])
        entity = entity_link.split("resource/")[1]
        return real_work(entity)
    else:
        return real_work(entity)

def real_work(entity):
    response = requests.get(host.format(entity)).content
    response = json.loads(response)
    if response.get('baidubaike', '') == '':
        contents = response['hudongbaike']
    else:
        contents = response.get('baidubaike', '')
    if contents == '':
        return []
    externalLink = contents['externalLink']
    print(externalLink)
    for link in externalLink:
        print(link)
    print(len(externalLink))
    return externalLink

if __name__ == '__main__':
    get_related_urls("奥巴马")