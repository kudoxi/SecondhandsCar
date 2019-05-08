from django.shortcuts import render
from django.http import request,HttpResponse
from . import models
import random
# Create your views here.
def test(req):
    #创建数据
    # models.Foo.objects.create(caption='ttt')
    # models.Foo.objects.create(caption='aaa')
    # models.Foo.objects.create(caption='wwe')
    # models.UserType.objects.create(title = '2b用户',fo_id=1)
    # models.UserType.objects.create(title = '普通用户',fo_id=2)
    # models.UserType.objects.create(title = 'nb用户',fo_id=3)
    # models.UserInfo.objects.create(name='aaa',age=12,ut_id=1)
    # models.UserInfo.objects.create(name='bbb',age=16,ut_id=2)
    # models.UserInfo.objects.create(name='ccc',age=14,ut_id=3)
    # models.UserInfo.objects.create(name='ddd',age=14,ut_id=3)
    # models.UserInfo.objects.create(name='eee',age=16,ut_id=2)

    # for i in range(100):
    #     name = 'root'+ str(i)
    #     models.UserInfo.objects.create(name=name, age=16, ut_id=random.choice([1,2,3]))
    #获取数据
    res = models.UserInfo.objects.all()
    for i in res:
        print('name',i.name)
        print('age',i.age)
        print('utid',i.ut_id)
        print('utype',i.ut.title)
        #print('caption',i.ut.fo.caption)

    #查看第一条
    res0 = models.UserInfo.objects.all().first()
    print('name', res0.name)
    print('age', res0.age)
    print('utid', res0.ut_id)
    print('utype', res0.ut.title)
    #print('caption', i.ut.fo.caption)

    #反向查询
    res1 = models.UserType.objects.all().first()
    #属于某一用户类型的所有用户
    for i in res1.userinfo_set.all():
        print(res1.title,i.name)


    #只查询个别字段_返回携带字典的QuerySet
    res2 = models.UserInfo.objects.all().values('name','age','ut__title')#QuerySet[{'name':'aaa','age':12}]
    for i in res2:
        print(i,type(i))
        print('name',i['name'])
        print('age',i['age'])
        print('ut__title',i['ut__title'])
        #print('ut',i.ut.title) 报错提示不存在

    #只查询个别字段_返回携带元组的QuerySet
    res3 = models.UserInfo.objects.all().values_list('name', 'age')#QuerySet[('aaa',12),('ccc',23)]
    for i in res3:
        print(i)
        print('name',i[0])
        print('age',i[1])

    return HttpResponse("aasa")


from django.core.paginator import Page,Paginator,PageNotAnInteger,EmptyPage
def test_page(req):
    params = {}
    current_page = req.GET.get('page')
    userlist = models.UserInfo.objects.all()

    page_obj = Paginator(userlist,10)
    '''page_obj
    per_page:每页显示条目数量
    count：数据总数
    num_pages :总页数
    page_range:总页数的索引范围 如（1,100）
    page:page对象
    '''

    try:
        posts = page_obj.page(current_page)#当前显示第几页
    except PageNotAnInteger as e:          #判断非整数传参
        posts = page_obj.page(1)
    except EmptyPage as e:                 #判断负数和空
        posts = page_obj.page(1)
    '''posts
    has_next                    是否有下一页
    next_page_number            下一页页码
    has_previous                是否有上一页
    previous_page_number        上一页页码
    object_list                 分页之后的数据列表
    number                      当前页
    '''
    params['userlist'] = posts
    return render(req,'test_page.html',params)

import math
class PageInfo(object):
    '''
    current_page:当前页
    per_page：每页显示数量
    QuerySet：sql查询出的QuerySet对象
    url_path：分页跳转路径
    max_page：显示的分页器最多数量，-1则全显示

    views方法里，将PageInfo构造后，传到template html页面，调用{{pageinfo.get_page}}即可显示,样式在css里设置
    ul的class:k_page_ul
    上一页a标签的class:k_page_pre
    页码a标签的class:k_page
    下一页a标签的class:k_page_next
    当前页li标签class: k_current_page
    '''
    def __init__(self,current_page,per_page,QuerySet,url_path,max_page=-1,*args,**kwargs):
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1

        self.per_page = per_page
        self.QuerySet = QuerySet
        self.url_path = url_path
        self.max_page = max_page

    # 第一页，0～10 不包括10
    # 第二页，10～20 不包括20
    # ...
    def start(self):
        return (self.current_page - 1) * self.per_page

    def end(self):
        return self.current_page * self.per_page

    def page_num(self):
        total_num = self.QuerySet.count()
        return math.ceil(total_num / self.per_page)

    def get_list(self):
        return self.QuerySet[self.start():self.end()]

    def get_page(self):
        total_page = self.page_num()
        print(self.max_page,total_page)
        if self.max_page > total_page or self.max_page == -1:
            self.max_page = total_page

        prepage_num = math.ceil((self.max_page - 1)/2)#当前页 的前面有多少页码
        aftpage_num = (self.max_page - 1) - prepage_num #当前页 的后面有多少页码
        if self.current_page - prepage_num <= 0:
            #如果前面没那么多页，前面有多少页，显示多少
            prepage_num = self.current_page - 1
            #后面的页码来补位
            aftpage_num = self.max_page - 1 - prepage_num

        if self.current_page + aftpage_num > total_page:
            #超出页码
            prepage_num = prepage_num + aftpage_num

        #页码放入数组以便遍历
        pages = [self.current_page]
        if prepage_num != 0:
            pre_page = -1
            for i in range(prepage_num):
                if pre_page==-1:
                    pre_page = self.current_page - 1
                else:
                    pre_page -=1
                if pre_page > 0 and pre_page not in pages:
                    pages.append(pre_page)
        if aftpage_num != 0:
            aft_page = -1
            for k in range(aftpage_num):
                if aft_page == -1:
                    aft_page = self.current_page + 1
                else:
                    aft_page += 1
                if aft_page <= total_page and aft_page not in pages:
                    pages.append(aft_page)

        pages = sorted(pages,reverse=False)

        #分页器
        pages_html = '<ul class="k_page_ul">'
        pre_num = self.current_page - 1
        next_num = self.current_page + 1
        #上一页
        url = self.url_path + '?page={}'
        if self.current_page != 1:
            pages_html += '<li><a class="k_page_pre" href="' + url.format(str(pre_num)) + '">上一页</a></li>'
        #中间页码
        for i in pages:
            current_class = 'k_current_page' if self.current_page == i else ''
            pages_html += '<li class="'+current_class+'"><a class="k_page" href="'+url.format(str(i))+'">'+str(i)+'</a></li>'
        #下一页
        if self.current_page != total_page :
            pages_html += '<li><a class="k_page_next" href="' + url.format(str(next_num)) + '">下一页</a></li>'

        return pages_html+"</ul>"

def test_page_self(req):
    params = {}
    user_obj = models.UserInfo.objects.all()
    print(type(user_obj))
    page_obj = PageInfo(req.GET.get('page'),10,user_obj,req.path,5)
    userlist = page_obj.get_list()
    params['userlist'] = userlist
    params['page_obj'] = page_obj
    return render(req,'test_page_self.html',params)