from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
ROLE_CHOICES = (
    (0,'卖家'),
    (1,'买家'),
)
SEX_CHOICES = (
    (0, '男'),
    (1, '女'),
)
BANK_CHOICES = (
    (0, '未绑定'),
    (1, '中国建设银行'),
    (2, '中国农业银行'),
    (3, '招商银行'),
    (4, '中国银行'),
)
#用户表
class UserInfo(AbstractUser):
    #我们想要一个继承后台用户表字段和相关分组,权限表,但是独立于后台用户表的UserInfo表
    #用户名密码直接用django自带的,不写
    #角色-不用django自带的
    role = models.IntegerField(verbose_name="角色",choices=ROLE_CHOICES,default=0)
    #isActive-不用django自带的
    isActive = models.BooleanField(verbose_name="是否激活",default=True)
    #isBan
    isBan = models.BooleanField(verbose_name="是否禁用",default=False)

    def __str__(self):
        return self.username

# 个人信息表
class DetailInfo(models.Model):
    user = models.OneToOneField(UserInfo,verbose_name="用户")
    realname = models.CharField(verbose_name="真实姓名",max_length=64,null=False)
    age = models.IntegerField(verbose_name="年龄")
    ads = models.TextField(verbose_name="地址")
    identity = models.CharField(max_length=18,null=False,verbose_name="身份证")
    sex = models.IntegerField(choices=SEX_CHOICES,default=0,verbose_name="性别")
    email = models.EmailField(verbose_name="邮箱")
    cellphone = models.CharField(max_length=20,null=False,verbose_name="手机号")

    def __str__(self):
        return self.user.username

    def get_sex(self):
        return u"男" if self.sex == 0 else u"女"

    def get_detail_url(self):
        return "xxxx.xxxx.com/xxx/id="+self.id

    class Meta:
        verbose_name = "用户信息列表"
        verbose_name_plural = "用户信息"


#银行表
class Bank(models.Model):
    user = models.ForeignKey(UserInfo,verbose_name="用户")
    bankNo = models.CharField(max_length=64,verbose_name="卡号",null=False)
    bank = models.IntegerField(choices=BANK_CHOICES,verbose_name="银行",default=0)
    bankpwd = models.CharField(verbose_name="交易密码",max_length=200,null=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "银行信息列表"
        verbose_name_plural = "银行信息"

#消息记录表
class Message(models.Model):
    user = models.ForeignKey(UserInfo,verbose_name="用户")
    message = models.TextField(verbose_name="消息内容")
    datetime = models.DateTimeField(verbose_name="时间",auto_now_add=True)
    isRead = models.BooleanField(verbose_name="是否已读",default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "消息记录列表"
        verbose_name_plural = "消息记录"