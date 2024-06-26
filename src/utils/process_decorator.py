from src.utils.database.read_data import read_data
import src.utils.config as config

def process_decorator(func):
    def wrapper(content):
        banurl = read_data(config.conn, "ban", None, None)
        banurl = [item[0] for item in banurl]
        if content['url'] == '/link/':
            comment = content.get('comment').replace('  ', ' ')
            if 'name' in comment and 'avatar' in comment and 'descr' in comment and 'link' in comment:
                mail = content['mail']
                created = content['created']
                state = -98

                data = func(comment)

                banlink = data['link'].replace('https://', '').replace('http://', '').split('/')[0]
                banlink = '.'.join(banlink.split('.')[-2:])
                if banlink in banurl:
                    state = -99
                data.update({
                    'mail': mail,
                    'state': state,
                    'created': created
                })
                return data
        return None
    return wrapper
