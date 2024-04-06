import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
def send_mail(mail, data, smtp_message,subject_message):
    smtp_host = smtp_message["smtp_host"]
    sender_email = smtp_message["sender_email"]
    smtp_port = smtp_message["smtp_port"]
    smtp_secure = smtp_message["smtp_secure"]
    smtp_user = smtp_message["smtp_user"]
    smtp_password = smtp_message["smtp_pass"]
    to_address = mail

    if data[4] != "NONE" and data[4] != "" and data[4] is not None:
        siteshot = data[4]
    else:
        siteshot = "https://image.thum.io/get/width/400/crop/800/allowJPG/wait/20/noanimate/"+data[3]
    if data[5] == "-98":
        state = "审核中"
    elif data[5] == "-99":
        state = "审核拒绝"
    else:
        state = "审核通过"
    try:
        mail_msg = f"""
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <title>友链申请</title>
            </head>
            <body>
            <style>
            .panel {{
                        width: 600px;
                        height: 500px;
                        margin: 0 auto;
                        background: #66ccff;
                        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
                        border-radius: 5%;
                    }}
            .list {{
                        list-style: none;
                        padding-left: 0;
                        list-style-type: none;
                    }}
            </style>
            <div class="panel">
                <div style="text-align: center;padding-top: 5%;">
                    <div style="font-weight: bold;">{subject_message}</div>
                </div>
                <div style="text-indent: 2em;padding-top: 5%;">亲爱的站长：&nbsp;<span style="color: #0066FF;">{data[0]}</span> &nbsp;您好：
                    <div style="padding-top: 5%;">欢迎来本站添加友链</div>
                    <div style="padding-top: 2%;">您申请的信息为：</div>
                    <div style="text-align: center;padding-bottom: 2%;">
                        <ul style="list-style: none; padding-left: 0;">
                            <li style="list-style: none; text-align: left;">昵称：{data[0]}</li>
                            <li style="list-style: none; text-align: left;">头像：{data[1]}</li>
                            <li style="list-style: none; text-align: left;">描述：{data[2]}</li>
                            <li style="list-style: none; text-align: left;">链接：{data[3]}</li>
                            <li style="list-style: none; text-align: left;">友链截图：{siteshot}</li>
                            <li style="list-style: none; text-align: left;">状态：{state}</li>
                            <li style="list-style: none; text-align: left;">申请时间：{data[6]}</li>
                        </ul>
                    </div>
                    <div>假如你的信息错误，或者是想更新个人信息，<span style="color: red;">请重新添加友链，并进入审核</span></div>
                </div>
            </div>
            </body>
            </html>
            """
        msg = MIMEText(mail_msg, 'html', 'utf-8')
        msg['From'] = formataddr(["星の野",sender_email])
        msg['To'] = formataddr(["FK",to_address])
        msg['Subject'] = Header(subject_message, 'utf-8').encode()
        if smtp_secure:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user,[to_address,],msg.as_string())
        server.quit()
    except Exception:
        pass