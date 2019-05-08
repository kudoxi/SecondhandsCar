from django.db import models
from userinfo.models import UserInfo as ui
from sale.models import CarInfo as ci
# Create your models here.
ORDER_STATUS_CHOICES = (
    (0,"未支付"),
    (1,"已发货"),
    (2,"已收货"),
)

#购买意愿表
class Cart(models.Model):
    user = models.ForeignKey(ui,verbose_name="用户")
    car = models.ForeignKey(ci,verbose_name="汽车")
    brand = models.CharField(max_length=64,verbose_name="品牌",null=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="价格")
    mileage = models.IntegerField(verbose_name="公里数")

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = "购买意愿列表"
        verbose_name_plural = "购买意愿"

#订单表
class Order(models.Model):
    buy_user = models.ForeignKey(ui,verbose_name="买家",related_name="buser")
    sale_user = models.ForeignKey(ui,verbose_name="卖家",related_name="suser")
    brand = models.CharField(max_length=64,null=False,verbose_name="品牌")
    orderNo = models.CharField(max_length=64,null=False,verbose_name="订单号")
    ctitle = models.CharField(max_length=64,null=False,verbose_name="车名")
    orderStatus = models.IntegerField(choices=ORDER_STATUS_CHOICES,verbose_name="订单状态")
    isDeleted = models.BooleanField(verbose_name="是否删除", default=False)
    c_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    register_date = models.DateField(auto_now_add=False, verbose_name="上牌日期")
    engineNo = models.CharField(max_length=64, null=False, verbose_name="发动机号")
    mileage = models.IntegerField(verbose_name="公里数")
    maintenance = models.BooleanField(verbose_name="是否维修", default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    extractprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="成交价格")
    newprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="新车价格")
    picture = models.ImageField(upload_to="static/carinfo", default="normal.png", verbose_name="图片")
    formalities = models.BooleanField(verbose_name="是否办好手续", default=False)
    debt = models.BooleanField(verbose_name="是否有债务", default=False)
    promise = models.TextField(verbose_name="承诺")
    isPurchase = models.BooleanField(verbose_name="是否已出售", default=False)

    def __str__(self):
        return self.buy_user.username


    class Meta:
        verbose_name = "订单列表"
        verbose_name_plural = "订单"