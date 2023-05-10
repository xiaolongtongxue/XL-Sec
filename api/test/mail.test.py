# -*- coding: utf-8 -*-
import smtplib
import email.utils
from email.mime.text import MIMEText

message = MIMEText("我是邮件的内容")
message['To'] = email.utils.formataddr(('接收者显示的姓名', '848053352@qq.com'))
message['From'] = email.utils.formataddr(('发送者显示的姓名', 'tian_onmyway@foxmail.com'))
message['Subject'] = '我是邮件的标题'
server = smtplib.SMTP_SSL('smtp.qq.com', 465)
server.login('xiaolong_onmyway@qq.com', 'rdlcrrbnlrbxjiji')
server.set_debuglevel(False)
try:
    server.sendmail('xiaolong_onmyway@qq.com', ['848053352@qq.com'], msg=message.as_string())
    isSend = True
except smtplib.SMTPException as e:
    print("Check_Send Sending Failure.The Error message is :: " + str(e))
    isSend = False
finally:
    server.quit()

# # -*- coding: utf-8 -*-
# import smtplib
# import email.utils
# from email.mime.text import MIMEText
#
# message = MIMEText("我是邮件的内容")
# message['To'] = email.utils.formataddr(('接收者显示的姓名', 'receiever@qq.com'))
# message['From'] = email.utils.formataddr(('发送者显示的姓名', 'sender@foxmail.com'))
# message['Subject'] = '我是邮件的标题'
# server = smtplib.SMTP_SSL('smtp.qq.com', 465)
# server.login('xxlogin@qq.com', 'qq-mail-key)
# server.set_debuglevel(True)
# try:
#     server.sendmail('aaa@qq.com', ['bbb@qq.com'], msg=message.as_string())
# finally:
#     server.quit()