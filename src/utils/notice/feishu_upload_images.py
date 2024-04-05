import requests
from requests_toolbelt import MultipartEncoder
from src.utils.notice.feishu_notice import feishu_notice

def upload_feishu_image(feishu_token,mail,data):
    if data[1] != "NONE" and data[1] != "" and data[1] is not None:
        image_content = download_image(data[1])
        if image_content is not None:
            avatar = feish_uploadImage(image_content, feishu_token)
        else:
            avatar = "img_v2_9dd98485-2900-4d65-ada9-e31d1408dcfg"
    if data[4] != "NONE" and data[4] != "" and data[4] is not None:
        image_content = download_image(data[4])
        if image_content is not None:
            siteshot = feish_uploadImage(image_content, feishu_token)
        else:
            siteshot = "img_v2_9dd98485-2900-4d65-ada9-e31d1408dcfg"
    else:
        image_content = "https://image.thum.io/get/width/400/crop/800/allowJPG/wait/20/noanimate/"+data[3]
        image_content = download_image(image_content)
        if image_content is not None:
            siteshot = feish_uploadImage(image_content, feishu_token)
        else:
            siteshot = "img_v2_9dd98485-2900-4d65-ada9-e31d1408dcfg"
    feishu_notice("申请友链",data,mail,feishu_token,siteshot,avatar)
    
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