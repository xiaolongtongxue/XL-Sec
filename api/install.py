# -*- coding: utf-8 -*-
import codecs
import hashlib
import base64
import sys

from dao import MYSQL
from util.Filter import is_valid_phone, is_valid_email

from util.GetSalt import get_salt_code

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

username = get_salt_code(length=7)
password = get_salt_code(length=7)

phone_num = "12345678912"
email = "1@a.a"

is_phone = 0
is_email = 0

try:
    if sys.argv[1] == '--help' or sys.argv[1] == '-h' or sys.argv[1] == '--h':
        print("请按照以下参数传参，或者将执行默认参数，请按照先后顺序传入参数，否则可能导致校验无效：")
        print("Please pass in the following parameters, or default parameters will be executed. "
              "Please pass in the parameters in order, otherwise it may result in invalid verification:")
        print("     -username <username> 默认用户名为随机强口令 The default username is a random strong password")
        print("     -password <password> 默认密码为随机强口令 The default password is a random strong password")
        print("     -email <email_address> 默认邮箱地址为1@a.a 且email_check强制为0，即关闭 "
              "The default email address is 1@a.a And email_ "
              "Check is forced to 0, which means it is closed")
        print("     -phone <phone_num> 默认手机号为：12345678912 且phone_check强制为0，即关闭 "
              "The default phone number is 12345678912 and "
              "phone_ Check is forced to 0, which means it is closed")
        print("     -email_check <0 or 1> 默认为0，表示邮件检查关闭 The default is 0, indicating that email checking is turned off")
        print("     -phone_check <0 or 1> 默认为0，表示短信检查关闭 The default is 0, indicating that SMS check is turned off")
        print("---------------------------------------------")
        print("Demo:")
        print("python install.py -username admin123tt --password 741258963 -email aa50@163.com -phone 13699999999 "
              "-email_check 1")
        sys.exit()
    else:
        if len(sys.argv) % 2 == 0:
            print("传参格式错误")
            sys.exit()
except IndexError:
    print("您未传递任何参数，这边将按照默认参数执行")
    print("You have not passed any parameters. We will follow the default parameters here")

my_dict = {}

for i in range(0, len(sys.argv[1:]), 2):
    my_dict[sys.argv[1:][i]] = sys.argv[1:][i + 1]

in_phone = False
in_email = False
for key in my_dict:
    try:
        if key == '-username' or key == '--username':
            username = my_dict[key]
        elif key == '-password' or key == '--password':
            password = my_dict[key]
        elif key == '-email' or key == '--email':
            if is_valid_email(my_dict[key]):
                email = my_dict[key]
                in_email = True
        elif key == '-phone' or key == '--phone':
            if is_valid_phone(my_dict[key]):
                phone_num = my_dict[key]
                in_phone = True
        elif key == '-email_check' or key == '--email_check':
            if in_email:
                if int(my_dict[key]) == 0 or int(my_dict[key]) == 1:
                    is_email = my_dict[key]
        elif key == '-phone_check' or key == '--phone_check':
            if in_phone:
                if int(my_dict[key]) == 0 or int(my_dict[key]) == 1:
                    is_phone = my_dict[key]
    except TypeError:
        continue

salt = get_salt_code(length=30)
passwd_base = base64.b64encode(password.encode('utf-8')).decode()
passwd_secret = hashlib.sha512((passwd_base + salt).encode()).hexdigest()

sql = "INSERT INTO `w_users` (`username`,`password`,`salt`,`phone`,`email`,`remark`,`phone_check`,`email_check`) " \
      "VALUES (?, ?, ?, ?, ?, '初始化', ?, ?); "
res = MYSQL.sql_no_select(sql=sql, data=(username, passwd_secret, salt, phone_num, email, is_phone, is_email))

if res:
    print("您创建的新用户的信息如下，请妥善保存，密码仅展示一次：")
    print("The information of the new user you created is as follows. "
          "Please keep it properly and display the password only once:")
    print("用户名(username)：\t" + username)
    print("密码(password)：\t" + password + "\n")
    print("手机号为(The phone num is)：" + phone_num)
    print("邮箱地址为(The Email Address is)：" + email)
    print("手机号校验(Check by phone num is):\t" + "已开启(opened)" if int(is_phone) == 1 else "未开启(not opened)")
    print("邮箱地址校验(Check by email address is):\t" + "已开启(opened)" if int(is_email) == 1 else "未开启(not opened)")
else:
    print("数据库出错")
    print("Database Error")
