from django.db import models
from userinfo.models import UserInfo as ui
# Create your models here.
EXAMINE_CHOICE = (
    (0,"审核中"),
    (1,"审核通过"),
    (2,"审核未通过"),
)
#品牌
class Brand(models.Model):
    logo_brand = models.ImageField(upload_to='static/brand',verbose_name="logo标志",default="normal.png")
    btitle = models.CharField(max_length=64,null=False,verbose_name="名称")
    isDelete = models.BooleanField(verbose_name="是否删除",default=False)

    def __str__(self):
        return self.btitle

    class Meta:
        verbose_name = "汽车品牌列表"
        verbose_name_plural = "汽车品牌"

#车辆信息
class CarInfo(models.Model):
    user = models.ForeignKey(ui,verbose_name="用户")
    brand = models.ForeignKey(Brand,verbose_name="品牌")
    ctitle = models.CharField(max_length=64,verbose_name="车名")
    register_date = models.DateField(auto_now_add=False,verbose_name="上牌日期")
    engineNo = models.CharField(max_length=64,null=False,verbose_name="发动机号")
    mileage = models.IntegerField(verbose_name="公里数")
    maintenance = models.BooleanField(verbose_name="是否维修",default=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="价格")
    extractprice = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="成交价格")
    newprice = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="新车价格")
    picture = models.ImageField(upload_to="static/carinfo",default="normal.png",verbose_name="图片")
    formalities = models.BooleanField(verbose_name="是否办好手续",default=False)
    debt = models.BooleanField(verbose_name="是否有债务",default=False)
    promise = models.TextField(verbose_name="承诺")
    examine = models.IntegerField(choices=EXAMINE_CHOICE,default=0,verbose_name="审核进度")
    isPurchase = models.BooleanField(verbose_name="是否已出售",default=False)
    isDeleted = models.BooleanField(verbose_name="是否删除",default=False)

    def __str__(self):
        return '{}-{}'.format(self.brand,self.ctitle)

    class Meta:
        verbose_name = "车辆信息列表"
        verbose_name_plural = "车辆信息"
#
# class Production(models.Model):
#     user = models.ForeignKey(ui,verbose_name="卖家")
#     title = models.CharField(max_length=255,verbose_name="名称")
#     useway = models.CharField(max_length=64,verbose_name="用途和产出产品材质")
#     address = models.CharField(max_length=64,verbose_name="产地")
#     useway = models.CharField(max_length=64,verbose_name="行业")