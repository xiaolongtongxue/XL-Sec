import smtplib
import email.utils
from email.mime.text import MIMEText

from config import SMTP_SENDING_EMAIL, SMTP_LOGIN_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_KEY, PANEL_TITLE
from dao import MYSQL


def send_email(uid: str, ip: str, receiver: str, send_title: str, send_data: str, loginer: str = SMTP_LOGIN_EMAIL,
               sender: str = SMTP_SENDING_EMAIL, smtp_server: str = SMTP_SERVER, smtp_port: int = SMTP_PORT,
               smtp_key: str = SMTP_KEY):
    message = MIMEText(send_data, 'html')
    # receiver
    message['To'] = email.utils.formataddr(('receiver', receiver))
    # sender
    message['From'] = email.utils.formataddr(("来自 " + PANEL_TITLE + "的一份验证码", sender))
    message['Subject'] = send_title
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(loginer, smtp_key)
    server.set_debuglevel(False)
    try:
        server.sendmail(sender, [receiver], msg=message.as_string())
        isSend = True
        MYSQL.sql_no_select(
            sql="INSERT INTO `w_email_log` (`login_email`,`send_email`,`getter_email`,`send_data`,`ip`,`uid`) VALUES "
                "(?,?,?,?,?,?);",
            data=(loginer, sender, receiver, send_data, ip, uid))
    except smtplib.SMTPException as e:
        print("Check_Send Sending Failure.The Error message is :: " + str(e))
        isSend = False
    finally:
        server.quit()
    return isSend


def send_msg():
    return False
