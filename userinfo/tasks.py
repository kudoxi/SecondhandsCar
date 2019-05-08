from django.core.mail import send_mail
from SecondhandsCar.celery import app
from SecondhandsCar.settings import *

'''
send_email_task_run:邮箱发送任务
email_title:str,邮件标题
email_message:str,邮件内容
to_email_addr:list,收件人邮箱列表
from_email:str,发件人邮箱

'''
@app.task(name="userinfo.tasks.send_email_task_run")
def send_email_task_run(email_title,email_message,to_email_addr,from_email=DEFAULT_FROM_EMAIL,fail_silently=False):
    res = send_mail(email_title,email_message, from_email,to_email_addr, fail_silently=fail_silently)
    print("to_email_addr:",to_email_addr)
    print("send res:",res)