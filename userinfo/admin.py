from django.contrib import admin
from .models import *
# Register your models here.
#后台密码
#python
#tarena123
admin.site.register(UserInfo)
admin.site.register(DetailInfo)
admin.site.register(Bank)
admin.site.register(Message)