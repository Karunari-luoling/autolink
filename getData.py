import json
import os
import time
from shutil import copy
import schedule
import requests
import urllib3
from datetime import timezone
from datetime import datetime
import itertools
import operator


def getbaseurldb(url):
    print("远程链接")
    urllib3.disable_warnings()
    if os.access("./config/db.json", os.F_OK):
        os.remove("./config/db.json")
    file = requests.get(url, allow_redirects=True, verify=False)
    open("./config/db.json", 'wb').write(file.content)
    processdata()


def getbaselocaldb(url):
    print("本地链接")
    copy(url, './config/db.json')
    processdata()


def processdata():
    if os.path.exists('./config/autolink_back.json'):
        os.remove('./config/autolink_back.json')
    basedata = {
        "partners": [],
        "dangerous": [],
        "failed": []
    }

    if not os.path.exists('./config/autolink_back.json'):
        with open('./config/autolink_back.json', 'w', encoding='utf-8') as f:
            json.dump(basedata, f)

    if os.path.exists('./autolink.json'):
        os.remove('./autolink.json')

    with open("./config/custom.json", 'r', encoding='utf-8') as fw:
        banurl = fw.read()
        banurl = json.loads(banurl)['ban']
        banurl = ' '.join(map(str, banurl))
    for line in open("./config/db.json", 'r', encoding='utf-8', errors='ignore'):
        content = json.loads(line)
        if content['url'] == '/link/':
            if ' ' in content['comment']:
                content['comment'] = content['comment'].replace(' ', '')
            if 'name' and 'avatar' and 'descr' and 'link' in content['comment']:
                banlink = ''
                siteshot = None
                if 'codeclass' in content['comment']:
                    name = content['comment'].split("name:")[1].split("\n")[0]
                    avatar = content['comment'].split('avatar:')[1].split('\n')[0]
                    descr = content['comment'].split("descr:")[1].split('\n')[0]
                    link = content['comment'].split('link:')[1].split('\n')[0]
                    if ('https:' or 'http:') and '//' in link:
                        link = link.replace('//', 'https://')
                    if 'siteshot' in content['comment']:
                        siteshot = content['comment'].split('siteshot:')[1].split('\n')[0]
                else:
                    name = content['comment'].split("name:")[1].split("<br>avatar:")[0]
                    avatar = content['comment'].split('avatar:<ahref="')[1].split('">')[0]
                    descr = content['comment'].split("descr:")[1].split('<br>link:')[0]
                    link = content['comment'].split('link:<ahref="')[1].split('">')[0]
                if 'https://' in link:
                    banlink = link.replace('https://', '')
                if 'http://' in link:
                    banlink = link.replace('http://', '')
                if 'github.io' in banurl and 'github.io' in banlink:
                    continue
                if siteshot:
                    if banlink not in banurl:
                        data = {
                            'mail': content['mail'],
                            'created': content['created'],
                            'name': name,
                            'avatar': avatar,
                            'descr': descr,
                            'link': link,
                            'siteshot': siteshot
                        }
                        with open('./config/autolink_back.json', 'r', encoding='utf-8') as f:
                            contents = json.load(f)
                        contents['partners'].append(data)
                        with open('./config/autolink_back.json', 'w', encoding='utf-8') as f:
                            json.dump(contents, f, indent=4, ensure_ascii=False)
                else:
                    if banlink not in banurl:
                        data = {
                            'mail': content['mail'],
                            'created': content['created'],
                            'name': name,
                            'avatar': avatar,
                            'descr': descr,
                            'link': link
                        }
                        with open('./config/autolink_back.json', 'r', encoding='utf-8') as f:
                            contents = json.load(f)
                        contents['partners'].append(data)
                        with open('./config/autolink_back.json', 'w', encoding='utf-8') as f:
                            json.dump(contents, f, indent=4, ensure_ascii=False)
    custom()


def defold():
    with open('./config/autolink_back.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('./config/autolink_back.json', 'r', encoding='utf-8') as f:
        datas = json.load(f)
    times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def process_list(data, list_name):
        # 对列表进行排序，具有相同 mail 和 created 的元素会被分到同一组
        data[list_name].sort(key=operator.itemgetter('mail', 'created'))
        # 用 itertools.groupby 函数分组
        groups = itertools.groupby(data[list_name], key=operator.itemgetter('mail', 'created'))
        # 在每个组中，选择最后一个元素
        new_list = [list(group)[-1] for key, group in groups]
        return new_list

    new_partners = process_list(data, 'partners')
    new_failed = process_list(data, 'failed')
    new_dangerous = process_list(data, 'dangerous')

    data['partners'] = new_partners
    data['dangerous'] = new_dangerous
    data['failed'] = new_failed
    data['last_update'] = times
    for item in data['failed']:
        if item in data['partners']:
            data['partners'].remove(item)
        if item in data['dangerous']:
            data['dangerous'].remove(item)
    for item in data['dangerous']:
        if item in data['partners']:
            data['partners'].remove(item)
    with open('./config/autolink_back.json', 'w', encoding='utf-8') as f:
        json.dump(datas, f, indent=4, ensure_ascii=False)
    with open('./autolink.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    hexo_circle_of_friends()


def custom():
    with open('./config/autolink_back.json', 'r', encoding='utf-8') as f:
        autolink_back = json.load(f)
    with open('./config/custom.json', 'r', encoding='utf-8') as f:
        customs = json.load(f)
    if customs['partners'] != '[]':
        # 对custom.json中的partners进行处理
        for partner in customs['partners']:
            if 'created' not in partner:  # 如果伙伴没有'created'字段
                partner['created'] = int(datetime.now(timezone.utc).timestamp() * 1000)  # 获取当前时间戳（毫秒级）并添加到伙伴中

        # 判断autolink_back中partners的部分
        for partner in customs['partners']:
            email = partner['mail']
            found1 = False
            for autolink_partner in autolink_back['partners']:
                if autolink_partner['mail'] == email:
                    for key in ('siteshot', 'created', 'avatar', 'descr', 'link', 'name'):
                        if partner.get(key):
                            autolink_partner[key] = partner.get(key)
                    found1 = True
            if not found1:  # 如果邮箱不存在于autolink_back.json的partners中，则添加到autolink_back.json的partners中
                autolink_back['partners'].append(partner)

        autolink_back['partners'].sort(key=lambda x: datetime.fromtimestamp(x['created'] / 1000), reverse=False)

        with open('./config/autolink_back.json', 'w', encoding='utf-8') as f:
            json.dump(autolink_back, f, indent=4, ensure_ascii=False)
        with open('./config/custom.json', 'w', encoding='utf-8') as f:
            json.dump(customs, f, indent=4, ensure_ascii=False)

    if os.path.exists('./config/failed.json'):
        with open('./config/failed.json', 'r', encoding='utf-8') as f:
            failed = json.load(f)
        with open('./config/autolink_back.json', 'r', encoding='utf-8') as f:
            contents = json.load(f)
        contents['failed'] = failed
        with open('./config/autolink_back.json', 'w', encoding='utf-8') as f:
            json.dump(contents, f, indent=4, ensure_ascii=False)
    is_website_dangerous()
    defold()


def hexo_circle_of_friends():
    with open('./autolink.json', 'r', encoding='utf-8') as f:
        autolink = json.load(f)
    if autolink['partners'] != '[]':
        names = [item['name'] for item in autolink['partners']]
        links = [item['link'] for item in autolink['partners']]
        avatars = [item['avatar'] for item in autolink['partners']]
        friends = list(zip(names, links, avatars))
        new_data = {'friends': friends}
    if autolink['dangerous'] != '[]':
        names = [item['name'] for item in autolink['dangerous']]
        links = [item['link'] for item in autolink['dangerous']]
        avatars = [item['avatar'] for item in autolink['dangerous']]
        dangerous = list(zip(names, links, avatars))
        new_data["friends"].extend(dangerous)
    with open('./hexo_circle_of_friends.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)


def is_website_dangerous():
    with open('./config/custom.json', 'r', encoding='utf-8') as f:
        customs = json.load(f)
    if customs['dangerous'] != '[]':
        with open('./config/autolink_back.json', 'r', encoding='utf-8') as f:
            dangerous = json.load(f)
        for partner in dangerous['partners']:
            link = partner.get('link')
            if link in customs['dangerous']:
                dangerous['dangerous'].append(partner)
        with open('./config/autolink_back.json', 'w', encoding='utf-8') as f:
            json.dump(dangerous, f, indent=4, ensure_ascii=False)


def is_website_alive():
    if os.path.exists('./config/failed.json'):
        os.remove('./config/failed.json')
    contents = []
    with open('./autolink.json', encoding='utf-8') as f:
        datas = json.load(f)
    links = []
    for key, value in datas.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and 'link' in item:
                    data = {
                        'mail': item['mail'],
                        'created': item['created'],
                        'name': item['name'],
                        'avatar': item['avatar'],
                        'descr': item['descr'],
                        'link': item['link']
                    }
                    try:
                        print(item['link'])
                        response = requests.request("GET", "https://v2.api-m.com/api/speed?url=" + item['link'],
                                                    headers={
                                                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'})
                        response = json.loads(response.text)
                        if response["code"] == 200:
                            print(item['link'] + ' 状态:' + str(response["code"]))
                        else:
                            print(item['link'] + ' 状态:' + str(response["code"]))
                            contents.append(data)
                            with open('./config/failed.json', 'w', encoding='utf-8') as f:
                                json.dump(contents, f, indent=4, ensure_ascii=False)
                    except requests.exceptions.RequestException as e:
                        print(f"Error occurred: {e}")
                        contents.append(data)
                        with open('./config/failed.json', 'w', encoding='utf-8') as f:
                            json.dump(contents, f, indent=4, ensure_ascii=False)
    print("检测完成")
    custom()


if __name__ == "__main__":
    try:
        with open("./config/config.json", 'r') as f:
            config = json.load(f)
            url = config['url']
            port = config['port']
            fentch_interval = config['fentch_interval']
            dangerous_interval = config["dangerous_interval"]
            failed_interval = config["failed_interval"]
    except:
        print("获取配置出错")
    if 'http' in url:
        schedule.every(fentch_interval).minutes.do(getbaseurldb, url)
        # schedule.every(failed_interval).hours.do(is_website_alive)
        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        schedule.every(fentch_interval).minutes.do(getbaselocaldb, url)
        # schedule.every(failed_interval).hours.do(is_website_alive)
        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(60)
