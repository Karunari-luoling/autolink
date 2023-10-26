import json
import os
import time
from multiprocessing import Process
from shutil import copy
import schedule
import requests
import urllib3
from datetime import timezone
from datetime import datetime


def getbaseurldb(url):
    print("远程链接")
    urllib3.disable_warnings()
    if os.access("config/db.json", os.F_OK):
        os.remove("config/db.json")
    file = requests.get(url, allow_redirects=True, verify=False)
    open("config/db.json", 'wb').write(file.content)
    processdata()


def getbaselocaldb(url):
    print("本地链接")
    copy(url, 'config/db.json')
    processdata()


def processdata():
    if os.path.exists('config/autolink_back.json'):
        os.remove('config/autolink_back.json')
    basedata = {
        "partners": [],
        "dangerous": [],
        "failed": []
    }
    if not os.path.exists('config/js_data.json'):
        with open('config/js_data.json', 'w', encoding='utf-8') as f:
            json.dump(basedata, f)
    if not os.path.exists('config/autolink_back.json'):
        with open('config/autolink_back.json', 'w', encoding='utf-8') as f:
            json.dump(basedata, f)

    if os.path.exists('./autolink.json'):
        os.remove('./autolink.json')

    with open("config/custom.json", 'r', encoding='utf-8') as fw:
        banurl = fw.read()
        banurl = json.loads(banurl)['ban']
        banurl = ' '.join(map(str, banurl))
    for line in open("config/db.json", 'r', encoding='utf-8', errors='ignore'):
        content = json.loads(line)
        if content['url'] == '/link/':
            if ' ' in content['comment']:
                content['comment'] = content['comment'].replace(' ', '')
            if 'name' and 'avatar' and 'descr' and 'link' in content['comment']:
                banlink, siteshot = '', ''
                if 'siteshot' in content['comment']:
                    # siteshot = content['comment'].split('link:<ahref="')[1].split('">')[0]
                    print("true")
                name = content['comment'].split("name:")[1].split("<br>avatar:")[0]
                avatar = content['comment'].split('avatar:<ahref="')[1].split('">')[0]
                descr = content['comment'].split("descr:")[1].split('<br>link:')[0]
                link = content['comment'].split('link:<ahref="')[1].split('">')[0]
                if 'https://' in link:
                    banlink = link.replace('https:', '').replace('/', '')
                if 'http://' in link:
                    banlink = link.replace('http:', '').replace('/', '')
                if 'github.io' in banurl and 'github.io' in banlink:
                    continue
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
                    with open('config/js_data.json', 'r', encoding='utf-8') as f:
                        contents = json.load(f)
                    contents['partners'].append(data)
                    with open('config/js_data.json', 'w', encoding='utf-8') as f:
                        json.dump(contents, f, indent=4, ensure_ascii=False)
                    with open('config/autolink_back.json', 'r', encoding='utf-8') as f:
                        contents = json.load(f)
                    contents['partners'].append(data)
                    with open('config/autolink_back.json', 'w', encoding='utf-8') as f:
                        json.dump(contents, f, indent=4, ensure_ascii=False)
    if os.path.exists('config/failed.json'):
        with open('config/failed.json', 'r', encoding='utf-8') as f:
            failed = json.load(f)
        with open('config/js_data.json', 'r', encoding='utf-8') as f:
            contents = json.load(f)
        contents['failed'] = failed
        with open('config/js_data.json', 'w', encoding='utf-8') as f:
            json.dump(contents, f, indent=4, ensure_ascii=False)
    if os.path.exists('./dangerous.json'):
        with open('config/dangerous.json', 'r', encoding='utf-8') as f:
            dangerous = json.load(f)
        with open('config/js_data.json', 'r', encoding='utf-8') as f:
            contents = json.load(f)
        contents['dangerous'] = dangerous
        with open('config/js_data.json', 'w', encoding='utf-8') as f:
            json.dump(contents, f, indent=4, ensure_ascii=False)
    defold()


def defold():
    with open('config/js_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('config/autolink_back.json', 'r', encoding='utf-8') as f:
        data_back = json.load(f)

    def process_list(data, list_name):
        new_list = [item for item in data[list_name] if not any(
            other['mail'] == item['mail'] and other['created'] > item['created'] for other in data[list_name])]
        return new_list

    new_partners = process_list(data, 'partners')
    new_failed = process_list(data, 'failed')
    new_dangerous = process_list(data, 'dangerous')
    new_partners_back = process_list(data_back, 'partners')

    data['partners'] = new_partners
    data['dangerous'] = new_dangerous
    data['failed'] = new_failed
    data_back['partners'] = new_partners_back
    for item in data['failed']:
        if item in data['partners']:
            data['partners'].remove(item)
        if item in data['dangerous']:
            data['dangerous'].remove(item)
    for item in data['dangerous']:
        if item in data['partners']:
            data['partners'].remove(item)
    with open('./autolink.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    with open('config/autolink_back.json', 'w', encoding='utf-8') as f:
        json.dump(data_back, f, indent=4, ensure_ascii=False)
    os.remove("config/js_data.json")
    custom()


def is_website_alive():
    if os.path.exists('config/failed.json'):
        os.remove('config/failed.json')
    contents = []
    with open('config/autolink_back.json', encoding='utf-8') as f:
        datas = json.load(f)
    links = []
    for key, value in datas.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and 'link' in item:
                    links.append(item['link'])
                    data = {
                        'mail': item['mail'],
                        'created': item['created'],
                        'name': item['name'],
                        'avatar': item['avatar'],
                        'descr': item['descr'],
                        'link': item['link']
                    }
                    try:
                        response = requests.head(item['link'], allow_redirects=True, timeout=5)
                        if response.status_code == 200:
                            # print(item['link'] + '状态:' + str(response.status_code))
                            return True
                        else:
                            contents.append(data)
                            with open('config/failed.json', 'w', encoding='utf-8') as f:
                                json.dump(contents, f, indent=4, ensure_ascii=False)
                    except requests.exceptions.RequestException as e:
                        print(f"Error occurred: {e}")
                        contents.append(data)
                        with open('config/failed.json', 'w', encoding='utf-8') as f:
                            json.dump(contents, f, indent=4, ensure_ascii=False)


def get_response_time():
    if os.path.exists('config/dangerous.json'):
        os.remove('config/dangerous.json')
    if os.path.exists('config/failed.json'):
        os.remove('config/failed.json')
    contents = []
    with open('config/autolink_back.json', encoding='utf-8') as f:
        datas = json.load(f)
    links = []
    for key, value in datas.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and 'link' in item:
                    links.append(item['link'])
                    data = {
                        'mail': item['mail'],
                        'created': item['created'],
                        'name': item['name'],
                        'avatar': item['avatar'],
                        'descr': item['descr'],
                        'link': item['link']
                    }
                    try:
                        response = requests.get(url=item['link']).elapsed.total_seconds()
                        # print(item['link'] + '响应时间:' + str(response))  # 时间为秒
                        if response > 5:
                            contents.append(data)
                            with open('./dangerous.json', 'w', encoding='utf-8') as f:
                                json.dump(contents, f, indent=4, ensure_ascii=False)
                    except requests.exceptions.RequestException as e:
                        # print(f"Error occurred: {e}")
                        contents.append(data)
                        print(contents)
                        with open('config/failed.json', 'w', encoding='utf-8') as f:
                            json.dump(contents, f, indent=4, ensure_ascii=False)


def custom():
    with open('./autolink.json', 'r', encoding='utf-8') as f:
        autolink = json.load(f)
    with open('config/custom.json', 'r', encoding='utf-8') as f:
        custom = json.load(f)
    if custom['partners'] != '[]':
        # 对custom.json中的partners进行处理
        for partner in custom['partners']:
            if 'created' not in partner:  # 如果伙伴没有'created'字段
                partner['created'] = int(datetime.now(timezone.utc).timestamp() * 1000)  # 获取当前时间戳（毫秒级）并添加到伙伴中

        for partner in custom['partners']:
            email = partner['mail']
            found = False
            for autolink_partner in autolink['partners']:
                if autolink_partner['mail'] == email:
                    if partner['siteshot'] != '':
                        autolink_partner['siteshot'] = partner['siteshot']  # 替换已存在的伙伴的'siteshot'字段
                    if partner['created'] != '':
                        autolink_partner['created'] = partner['created']
                    found = True
                    break
            if not found:  # 如果邮件不存在于autolink.json的partners中，则添加到autolink.json的partners中
                autolink['partners'].append(partner)

        autolink['partners'].sort(key=lambda x: datetime.fromtimestamp(x['created'] / 1000), reverse=False)

        with open('./autolink.json', 'w', encoding='utf-8') as f:
            json.dump(autolink, f, indent=4, ensure_ascii=False)
        with open('config/custom.json', 'w', encoding='utf-8') as f:
            json.dump(custom, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    try:
        with open("config/config.json", 'r') as f:
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
        schedule.every(failed_interval).hours.do(is_website_alive)
        schedule.every(dangerous_interval).hours.do(get_response_time)
        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        schedule.every(fentch_interval).minutes.do(getbaselocaldb, url)
        schedule.every(failed_interval).hours.do(is_website_alive)
        schedule.every(dangerous_interval).hours.do(get_response_time)
        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(60)
