from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist,ValidationError
import json
import datetime
import logging
from .models import *
from SecondhandsCar.settings import *
from django.contrib.auth.hashers import make_password,check_password
from .userDecorator import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import re
from django.template.loader import render_to_string
import weasyprint
import random
from .tasks import send_email_task_run
# Create your views here.

#注册
def register(req):
    params = {}
    return render(req,"register.html")

#注册ajax
def doregister(req):
    #salt = 'k_atja'
    params = {}
    usertype = req.POST.get("usertype")
    email = req.POST.get("email")
    validcode = req.POST.get("validcode")
    username = req.POST.get("username")
    password = req.POST.get("password")
    rep = HttpResponse("邮箱验证码")
    cook_email = req.session.get("v_email")
    cook_code = req.session.get("v_code")
    #判断验证码是否正确
    if not (cook_email == email and cook_code == validcode):
        print(cook_email,email)
        print(cook_code, validcode)
        params['error'] = "验证码错误"
        params['code'] = 201
    #邮箱是否存在
    elif UserInfo.objects.filter(email = email).exists():
        params['error'] = "邮箱已存在"
        params['code'] = 201
    # 判断用户是否存在
    elif UserInfo.objects.filter(username = username).exists():
        params['error'] = "用户已存在"
        params['code'] = 201
    else:
        # 密码加密
        password = make_password(password,None,'pbkdf2_sha1')
        #加入数据库
        UserInfo.objects.create(
            username = username,
            password = password,
            email = email,
            role = usertype
        )
        params['error'] = ""
        params['code'] = 101

    return HttpResponse(json.dumps(params), content_type='application/json')

#登录
@have_login
def login(req):
    #if req.user.is_authenticated():
    #    return HttpResponseRedirect('/userinfo/usercenter/')
    return render(req,"login.html")

#登录ajax
def dologin(req):
    params = {}
    source_url = req.COOKIES.get("source_url")
    if not source_url:
        source_url = "userinfo/usercenter"
    uname = req.POST.get("username")
    pwd = req.POST.get("password")
    validcode = req.POST.get("validcode")
    remember = req.POST.get("remember")
    if uname == "":
        params['error'] = "用户为空"
        params['code'] = 201
    elif pwd == "":
        params['error'] = "密码为空"
        params['code'] = 201
    elif validcode == "":
        params['error'] = "验证码为空"
        params['code'] = 201
    elif validcode.lower() != req.session.get('validcode').lower():
        print(validcode,req.session.get('validcode'))
        params['error'] = "验证码错误"
        params['code'] = 201
    else:
        # 密码无需加密,自动比对用户名和密码是否在数据库并且是否正确,正确则直接返回对象,错误则空,
        # 能用这个方法的前提是,用户表继承了后台的用户表
        user = auth.authenticate(username=uname,password=pwd)
        if user is not None and user.is_active:
            # django 自动存放session cookie
            #auth.login(req,user) #这种的session和cookie会和后台的混淆
            req.session['fuserid'] = user.id
            req.session['fusername'] = user.username
            response = HttpResponse('remember')
            if remember != "false":
                response.set_cookie("fuserid",user.id)
                response.set_cookie("fusername",user.username)
            params['source_url'] = source_url
            params['error'] = ""
            params['code'] = 101
        else:
            params['error'] = "用户不存在或已被禁用"
            params['code'] = 201

    return HttpResponse(json.dumps(params), content_type='application/json')

#登出
def logout_(req):
    #auth.logout(req)
    del req.session['fuserid']
    del req.session['fusername']
    response = HttpResponse('remember')
    response.set_cookie("fuserid","",-1)
    response.set_cookie("fusername","",-1)
    return HttpResponseRedirect("/userinfo/login/")


@log_in
def usercenter(req):
    return render(req,"usercenter.html")


#生成pdf
def dopdf(req):
    qr = "hello world"
    html = render_to_string('login.html',{'qr':qr})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\"mymodel.pdf\"'
    weasyprint.HTML(string=html).write_pdf(response)
    return response

#获取邮箱验证码
def email_valicode(req):
    params = {}
    to_email_addr = []
    email = req.POST.get("email")
    to_email_addr.append(email)
    if not email:
        params['error'] = "邮箱不存在"
        params['code'] = 201

    random_num = ""
    for i in range(5):
        random_num += str(random.randint(0, 9))
    email_title = "庞械城邮箱验证码"
    email_message = "您的验证码:"+random_num+";如不是本人请忽略."
    result = send_email_task_run.delay(email_title,email_message,to_email_addr)
    print("***********",result)
    params['error'] = ""
    params['code'] = 101
    print(random_num)
    req.session["v_email"] = email
    req.session["v_code"] = random_num

    return HttpResponse(json.dumps(params), content_type='application/json')