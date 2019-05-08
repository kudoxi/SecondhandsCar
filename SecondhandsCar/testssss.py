import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from socket import error as SocketError
import errno
my_sender='1140514109@qq.com'
my_pass = 'zuxwkvwwqjhhhdbh'#zuxwkvwwqjhhhdbh
my_user = '1140514109@qq.com'


def mail():
    ret = True
    try:
        msg = MIMEText('填写邮件内容smtp密码:zuxwkvwwqjhhhdbh', 'plain', 'utf-8')
        msg['From'] = formataddr(["sender", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["getter", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "菜鸟教程发送邮件测试"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    # except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
    #     ret = False
    #     print(e)
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise
        print(e)
        ret = False
    return ret


ret = mail()
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")
#zuxwkvwwqjhhhdbh