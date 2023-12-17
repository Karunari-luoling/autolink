import re
import yaml
from src.utils.database.read_data import read_data
import src.utils.config as config

def process_data(content):
    banurl = read_data(config.conn, "ban", None, None)
    banurl = [item[0] for item in banurl]
    if content['url'] == '/link/':
        comment = content.get('comment').replace('  ', ' ')
        if 'name' and 'avatar' and 'descr' and 'link' in comment:
            mail = content['mail']
            created = content['created']
            state = 2
            if 'code class' in comment:
                name = re.search(r'name: (.*?)\n', comment).group(1)
                avatar = re.search(r'avatar: (.*?)\n', comment).group(1)
                descr = re.search(r'descr: (.*?)\n', comment).group(1)
                link = re.search(r'link: (.*?)\n', comment).group(1)
                if link.endswith('/'):
                    link = link.rstrip('/')
                if ('https:' or 'http:') not in link:
                    if '//' in link:
                        link = link.replace('//', 'https://')
                    else :
                        link = 'https://' + link
                siteshot_match = re.search(r'siteshot: (.*?)\n', comment)
                siteshot = siteshot_match.group(1) if siteshot_match else None
            else:
                name = re.search(r'name: (.*?)<br>', comment).group(1)
                avatar = re.search(r'avatar: <a href="(.*?)">', comment).group(1)
                descr = re.search(r'descr: (.*?)<br>', comment).group(1)
                link = re.search(r'link: <a href="(.*?)">', comment).group(1)
                if link.endswith('/'):
                    link = link.rstrip('/')
                if ('https:' or 'http:') not in link:
                    if '//' in link:
                        link = link.replace('//', 'https://')
                    else :
                        link = 'https://' + link
                siteshot_match = re.search(r'siteshot: <a href="(.*?)">', comment)
                siteshot = siteshot_match.group(1) if siteshot_match else None

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
                        'state':state,
                        'created': created
                    }
            return data
    return None