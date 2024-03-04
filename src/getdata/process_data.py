from src.getdata.config import get_match, process_data_final, process_link
from src.utils.process_decorator import process_decorator

@process_decorator
def process_data(comment):
    fields = ['name', 'avatar', 'descr', 'link', 'siteshot']
    comment = comment.replace('：', ':').replace('&amp;', '&')
    for field in fields:
        comment = comment.replace(f'{field}: ', f'{field}:').replace(f'{field}:', f'{field}: ')
    if 'code class' in comment:
        name = get_match(r'name: (.*?)\n', comment)
        avatar = get_match(r'avatar: (.*?)\n', comment)
        descr = get_match(r'descr: (.*?)\n', comment)
        link = process_link(get_match(r'link: (.*?)\n', comment))
        siteshot = get_match(r'siteshot: (.*?)\n', comment)
    else:
        name = get_match(r'name: (.*?)<br>', comment)
        avatar = get_match(r'avatar: <a href="(.*?)">', comment)
        descr = get_match(r'descr: (.*?)<', comment)
        link = process_link(get_match(r'link: <a href="(.*?)">', comment))
        siteshot = get_match(r'siteshot: <a href="(.*?)">', comment)
    name, avatar, descr, siteshot = process_data_final(name, avatar, descr, siteshot)

    return {
                'name': name,
                'avatar': avatar,
                'descr': descr,
                'link': link,
                'siteshot': siteshot,
            }