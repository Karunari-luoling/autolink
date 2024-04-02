import requests
from requests_toolbelt import MultipartEncoder

def download_image(image_url):
    response = requests.head(image_url)

    if response.status_code == 200:
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content

    elif response.status_code == 404:
        return None
    
    else:
        response.raise_for_status()

def feish_uploadImage(image,token):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': image}
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer '+ token,
    }
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    return response.json()['data']['image_key']