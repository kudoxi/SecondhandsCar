from django.shortcuts import render
#from django.views import View
from django.views.generic import View
from django.http import HttpResponse
from .tasks import start_running
from time import sleep
# Create your views here.

class IdexView(View):
    def index(req):
        params = {}
        #商品列表


        return render(req,"index.html",params)



    #celery 测试
    def test2(req):
        print('>=====开始发送请求=====<')
        for i in range(10):
            print('>>',end='')
            sleep(0.1)

        start_running.delay('》》》》》我是传送过来的《《《《《')
        return HttpResponse('<h2> 请求已发送 </h2>')