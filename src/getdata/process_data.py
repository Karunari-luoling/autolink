import re
from bs4 import BeautifulSoup
import yaml
from src.utils.database.read_data import read_data
import src.utils.config as config

def process_data(content):
    banurl = read_data(config.conn, "ban", None, None)
    banurl = [item[0] for item in banurl]
    if content['url'] == '/link/':
        comment = content.get('comment')
        if 'name' and 'avatar' and 'descr' and 'link' in comment:
            if comment:
                soup = BeautifulSoup(comment, 'html.parser')
                mail = content['mail']
                state = 2
                ul = soup.find('ul')
                pre = soup.find('pre')
                if ul:
                    name = re.search(r'name: (.*?)<br>', comment).group(1)
                    avatar = re.search(r'avatar: <a href="(.*?)">', comment).group(1)
                    descr = re.search(r'descr: (.*?)<br>', comment).group(1)
                    link = re.search(r'link: <a href="(.*?)">', comment).group(1)
                    siteshot_match = re.search(r'siteshot: <a href="(.*?)">', comment)
                    siteshot = siteshot_match.group(1) if siteshot_match else None
                if pre:
                    yaml_data = yaml.safe_load(pre.text)
                    if yaml_data:
                        for data in yaml_data:
                            name = data.get('name')
                            link = data.get('link')
                            if ('https://' or 'http://') not in link:
                                if("//" in link):
                                    link = link.replace('//', 'https://')
                                else:
                                    link = 'https://' + link
                            avatar = data.get('avatar')
                            descr = data.get('descr')
                            siteshot = data.get('siteshot')
                banlink = link.replace('https://', '').replace('http://', '').split('/')[0]
                banlink = '.'.join(banlink.split('.')[-2:])
                if banlink in banurl:
                    state = 0
                data = {
                            'mail': mail,
                            'name': name,
                            'avatar': avatar,
                            'descr': descr,
                            'link': link,
                            'siteshot': siteshot,
                            'state':state
                        }
                return data
    return None