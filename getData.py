import json
import os
import time
from shutil import copy

import schedule
import requests
import urllib3


def getbaseurldb(url):
    print("远程链接")
    urllib3.disable_warnings()
    if os.access("./db.json", os.F_OK):
        os.remove("./db.json")
    file = requests.get(url, allow_redirects=True, verify=False)
    open("./db.json", 'wb').write(file.content)
    processdata()


def getbaselocaldb(url):
    print("本地链接")
    copy(url, './db.json')
    processdata()


def processdata():
    with open("./ban.json", 'r', encoding='utf-8') as fw:
        banurl = fw.read()
        banurl = json.loads(banurl)
        banurl = ' '.join(map(str, banurl))
    for line in open("./db.json", 'r', encoding='utf-8', errors='ignore'):
        content = json.loads(line)
        if content['url'] == '/link/':
            if ' ' in content['comment']:
                content['comment'] = content['comment'].replace(' ', '')
            if 'name' and 'avatar' and 'descr' and 'link' in content['comment']:
                banlink = ''
                name = content['comment'].split("name:")[1].split("<br>avatar:")[0]
                avatar = content['comment'].split('avatar:<ahref="')[1].split('">')[0]
                descr = content['comment'].split("descr:")[1].split('<br>link:')[0]
                link = content['comment'].split('link:<ahref="')[1].split('">')[0]
                if 'https://' in link:
                    banlink = link.replace('https:', '').replace('/','')
                if 'http://' in link:
                    banlink = link.replace('http:', '').replace('/','')
                if 'github.io' in banurl and 'github.io' in banlink:
                    continue
                if banlink not in banurl:
                    data = {
                        'mail': content['mail'],
                        'created': content['created'],
                        'name': name,
                        'avatar': avatar,
                        'descr': descr,
                        'link': link
                    }
                    with open("./js_data.json", 'a', encoding='utf-8') as fw:
                        autolink = json.dumps(data, indent=4, ensure_ascii=False)
                        fw.write(autolink + ',')
                        fw.write('\n')

    with open("./js_data.json", 'r', encoding='utf-8') as fw:
        content = fw.read()
        if '[' in content:
            content = content.replace("[", "")
            content = content.replace("]", ",")
            content = '[' + content + ']'
            content = content.replace(",\n]", "]\n")
        else:
            content = '[' + content + ']'
            content = content.replace(",\n]", "]\n")
    with open("./js_data.json", 'w', encoding='utf-8') as fw:
        fw.write(content)
    defold()


def defold():
    json_data = []
    k, m, n = 0, 0, 0
    with open("./js_data.json", 'r', encoding='utf-8') as fw:
        content = fw.read()
        content = json.loads(content)
        for i in content:
            for j in content:
                m += 1
                if i['mail'] == j['mail'] and i['created'] == j['created']:
                    k += 1
                elif i['mail'] == j['mail'] and i['created'] < j['created']:
                    json_data.append(j)
                elif i['mail'] == j['mail'] and i['created'] > j['created']:
                    continue
                else:
                    k += 1
            if k == m:
                json_data.append(i)
            m, k = 0, 0
    autolink = json.dumps(json_data, indent=4, ensure_ascii=False)
    links = []
    autolink = json.loads(autolink)
    with open("./autolink.json", 'w', encoding='utf-8') as fw:
        for link in autolink:
            if link in links:
                continue
            else:
                links.append(link)
        autolink = json.dumps(links, indent=4, ensure_ascii=False)
        fw.write(autolink)
    os.remove("./js_data.json")


if __name__ == "__main__":
    try:
        with open("./config.json", 'r') as f:
            config = json.load(f)
            url = config['url']
            port = config['port']
            interval = config['interval']
    except:
        print("获取配置出错")
    if 'http' in url:
        schedule.every(interval).minutes.do(getbaseurldb, url)
        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        schedule.every(interval).minutes.do(getbaselocaldb, url)
        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(60)
