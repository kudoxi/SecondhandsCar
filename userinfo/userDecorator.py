from django.http import HttpResponseRedirect,HttpResponse

'''身份认证装饰器，
:param func:
:return:
'''
def log_in(func):
    def wrapper(request,*args,**kwargs):
        fuserid = request.COOKIES.get("fuserid")
        fusername = request.COOKIES.get("fusername")
        if fuserid:
            request.session['fuserid'] = fuserid
        if fusername:
            request.session['fusername'] = fusername

        if not request.session.get("fuserid"):
            return HttpResponseRedirect("/userinfo/login/")
        return  func(request,*args, **kwargs)
    return wrapper


#已登录的不进入登录页面
def have_login(func):
    def wrapper(request,*args,**kwargs):
        source_url = request.COOKIES.get("source_url")
        if not source_url:
            source_url = "/userinfo/usercenter/"
        if request.session.get("fuserid"):
            return HttpResponseRedirect(source_url)
        return  func(request,*args, **kwargs)
    return wrapper