# 配置项说明
## config.yml
`/config/config.yml`
``` yml
basic_settings:
  db:
  # 选择你的twikoo数据库类型，目前只支持loacl
  - local: enable
    url: ./data/db.json.0
  - mongodb: disable
    url: mongodb://localhost:27017
  port: 3000 #项目运行端口
  debug: true #是否开启flask debug模式
  cors: true #是否开启跨域
  password: #api管理密码
  JWT_SECRET_KEY: hkxual.14na01hdw.2 #jwt密钥
fentch_time:
  fentch_interval: 30 #获取评论的间隔单位是分钟
  dangerous_interval: 24 #发送Get请求验证友链状态，间隔是小时，暂时不支持
  failed_interval: 6 #发送HEAD请求验证友链是否存活，间隔是小时，暂时不支持

```

# 接口说明
## /autolink
`ip/autolink`
此处返还你的友链json，你可以根据这个json去适配你的主题，第一个api不返回详细信息，第二个api当存在正确的Authorization时，会返回详细的友链内容
示例：
```js
fetch("ip/autolink")
  .then(response => response.json())
  .then(json => {
    console.log(json)
  }).catch(err => console.log('Request Failed', err));
```

```js
let token = localStorage.getItem('token')
fetch('ip/autolink',{
    method: 'POST',
    headers: {'Authorization': token},
  })
  .then(response => response.json())
  .then(json => {
    console.log(json)
  }).catch(err => console.log('Request Failed', err));
```
返回示例如下：
```json
{
    "partners": [
        {
            "avatar": "https://bu.dusays.com/2023/10/01/6519291503349.jpg",
            "descr": "我自是年少，韶华倾负",
            "link": "https:https://byer.top/",
            "mail": "1842105028@qq.com",
            "name": "星の野",
            "siteshot": null,
            "state": 2
        },
        {
            "avatar": "https://cdn.jsdelivr.net/gh/taosu0216/picgo/20230821231539.png",
            "descr": "Daily Growing",
            "link": "https:https://blog.yblue.top",
            "mail": "2412211487@qq.com",
            "name": "Taosu`Home",
            "siteshot": null,
            "state": 2
        },
        {
            "avatar": "https://ll.sc.cn/img/avatar.png",
            "descr": "爱生活，爱工作，爱折腾。",
            "link": "https:https://ll.sc.cn/",
            "mail": "i@ll.sc.cn",
            "name": "雷雷屋头",
            "siteshot": null,
            "state": 2
        },
        {
            "avatar": "https://s2.loli.net/2023/10/17/4GK2m3UkXztog9D.jpg",
            "descr": "知识匮乏，生活处处是魔法",
            "link": "https:https://blog.yesord.top",
            "mail": "2691004662@qq.com",
            "name": "PIKO",
            "siteshot": null,
            "state": 2
        }
    ]
}
```
state = 2 是正常访问的友链（1暂定为优先级最高，默认添加到2）
state = 0 是黑名单的友链
state = -1 是黑名单的友链

## /hexo_circle_of_friends
`ip/hexo_circle_of_friends`
此api是为友链朋友圈做的适配，可以使其正常抓取友链
示例：
```js
fetch("ip/hexo_circle_of_friends")
    .then(response => response.json())
    .then(json => {
        console.log(json)
    }).catch(err => console.log('Request Failed', err));
```
返回示例如下：
```json
{
    "friends": [
        [
            "星の野",
            "https://byer.top/",
            "https://bu.dusays.com/2023/10/01/6519291503349.jpg"
        ],
        [
            "Taosu`Home",
            "https://blog.yblue.top",
            "https://cdn.jsdelivr.net/gh/taosu0216/picgo/20230821231539.png"
        ],
        [
            "雷雷屋头",
            "https://ll.sc.cn/",
            "https://ll.sc.cn/img/avatar.png"
        ],
        [
            "Redish101 Blog",
            "https://blog.redish101.top",
            "https://blog.redish101.top/favicon.ico"
        ],
        [
            "PIKO",
            "https://blog.yesord.top",
            "https://s2.loli.net/2023/10/17/4GK2m3UkXztog9D.jpg"
        ],
        [
            "以太工坊",
            "https://www.zair.top/",
            "https://www.zair.top/img/logo.png"
        ]
    ]
}
```
友链朋友圈配置看下方链接
{% link 友链朋友圈, 点我前往！, https://fcircle-doc.yyyzyyyz.cn/#/settings %}

## /login
`ip/login`
此api用于登录，如果没有设置密码，则第一次登录密码将设为密码，返回token，自行储存到本地使用，有效期12h或后端重启
示例:
```js
fetch('ip/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({"password":"password"})
    })
    .then(response => response.json())
    .then(json => {
        if(json['code']==200){
            localStorage.setItem('token', json['access_token']);
        }
    }).catch(err => console.log('Request Failed', err));
```
返回示例:
```json
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMjMxMzYwMiwianRpIjoiMTA0OTg0ZmEtMDBlZS00ODk4LTg0NDMtNDk0Yzc2MjdlMGM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRodW5kZXJfbHVvbGluZyIsIm5iZiI6MTcwMjMxMzYwMiwiZXhwIjoxNzAyMzE0NTAyfQ.idyM7o91oLtEylSALNLxvxSSi6mZC0T7WCbEuSvDIPI",
"code": 200
}
```
## /insert_links
`ip/insert_links`
此api用于修改和提交友链，以及提交黑名单，处于黑名单时，以存在的友链的state为0
示例:
```js
let token = localStorage.getItem('token')
data = 
{
    "partners": 
        [{
            "avatar": "",
            "descr": "",
            "link": "",
            "mail": "",
            "name": "",
            "siteshot": "",
            "state": 2
        }],
    "ban": ["github.io"]
    // partners和ban一次只能提交一种，返回的是各自对应的值
}
fetch('ip/insert_links', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
        'Authorization': token
    },
    body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(json => {
        console.log(json)
    }).catch(err => console.log('Request Failed', err));
```
返回示例:
```json
//partners:
{
  "partners": [
    {
      "avatar": "https://bu.dusays.com/2023/10/01/6519291503349.jpg",
      "descr": "\u6211\u81ea\u662f\u5e74\u5c11\uff0c\u97f6\u534e\u503e\u8d1f",
      "id": 1,
      "link": "https:https://byer.top/",
      "mail": "1842105028@qq.com",
      "name": "\u661f\u306e\u91ce",
      "siteshot": null,
      "state": 2
    },
    {
      "avatar": "https://cdn.jsdelivr.net/gh/taosu0216/picgo/20230821231539.png",
      "descr": "Daily Growing",
      "id": 8,
      "link": "https:https://blog.yblue.top",
      "mail": "2412211487@qq.com",
      "name": "Taosu`Home",
      "siteshot": null,
      "state": 2
    }
  ]
}
//ban:
{
  "ban": [
    "github.io"
  ]
}
```
## /upload
`ip/upload`
此api用于在博客中给用户自己添加友链的权限，提交的友链的权限为-1，示例代码如下
```js
let obj = {
        "partners": [
          {
              "avatar": "",
              "descr": "",
              "link": "",
              "mail": "",
              "name": "",
              "siteshot": ""
          }
      ]
    };
fetch('ip/upload', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: obj
  })
  .then(response => response.json())
  .then(data => {
    console.log(json)
  }).catch(err => console.log('Request Failed', err));
```
返回示例：
```json
{"code": "err", "message": "There is no modified data"}
{"code": "ok", "message": "Data has been modified successfully"}
```

## /update_links
`ip/update_links`
此api用于修改友链的内容，提交需带上token和mail，其余内容随便
```js
let token = localStorage.getItem('token')
data = 
[{
  "link": "",
  "mail": ""
}]
fetch('ip/update_links', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
        'Authorization': token
    },
    body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(json => {
        console.log(json)
    }).catch(err => console.log('Request Failed', err));
```
输出如下:
```json
{"code": "200", "message": "Data has been modified successfully"}
{"code": "error", "message": "Missing 'mail' in data"}
```
## /config
`ip/config`
此api用于修改本地的配置文件
示例:
```js
let token = localStorage.getItem('token')
data = 
{
    "fentch_time.fentch_interval":30,
    "basic_settings.debug":"false"
}
fetch('ip/config', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
        'Authorization': token
    },
    body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(json => {
        console.log(json)
    }).catch(err => console.log('Request Failed', err));
```
返回示例:
```json
{
  "basic_settings": {
    "JWT_SECRET_KEY": "hkxual.14na01hdw.2",
    "cors": true,
    "db": [
      {
        "local": "enable",
        "url": "./data/db.json.0"
      },
      {
        "mongodb": "disable",
        "url": "mongodb://localhost:27017"
      }
    ],
    "debug": "false",
    "password": "***************",
    "port": 3000
  },
  "fentch_time": {
    "dangerous_interval": 24,
    "failed_interval": 6,
    "fentch_interval": 30
  }
}

```