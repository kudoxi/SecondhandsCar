from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from SecondhandsCar.settings import *
from django.http import HttpResponse
import random

def coderandom():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#获取验证码
def get_validcode_img(request):
    #color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    # 生成一个颜色随机的大小为160,30的图片
    img = Image.new(mode="RGB", size=(250, 50), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),128))
    # 设置图片的绘制颜色
    draw = ImageDraw.Draw(img, "RGB")
    # 设置图片的绘制字体（只写字体名，会默认在系统的Fonts下去找）
    font_path = os.path.join(BASE_DIR, "static", "font", "aguzlo.ttf")
    font = ImageFont.truetype(font_path, 28)
    #font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', 25)
    # font = ImageFont.truetype(r'C:\中文\kumo.ttf', 25)  # 中文路径无法识别

    # 设置图片上的字符串
    valid_list = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_letter_low = chr(random.randint(65, 90))
        random_letter_upper = chr(random.randint(96, 122))
        random_char = random.choice([random_num, random_letter_low, random_letter_upper])  # 随机选择字符（数字，大小写字母)
        # 通过draw.text方法，设置图片上字符串的x,y坐标，字符串，颜色，字体（for循环5次，生成5个字符的验证码)
        draw.text(xy=[50+i*35, 10], text=random_char, fill=(random.randint(0, 255), 255, random.randint(0, 255)), font=font)
        valid_list.append(random_char)

    #画干扰点
    for k in range(50):
        draw.point([random.randint(0,250),random.randint(0,50)],(random.randint(0, 255), 255, random.randint(0, 255)))
    #画干扰线
    for k in range(2):
        x1= random.randint(0,250)
        y1 = random.randint(0,50)
        x2= random.randint(0,250)
        y2 = random.randint(0,50)
        draw.line((x1,y1,x2,y2),(random.randint(0, 255), 255, random.randint(0, 255)),1)

    #画圆
    #draw.arc((x1,y1,x1+10,y1+10),0,180,(random.randint(0, 255), 255, random.randint(0, 255)))
    # 获取一个内存中的文件句柄
    f = BytesIO()
    # 在文件句柄中写入文件
    img.save(f, 'png')
    # 取出文件
    data = f.getvalue()
    # 转换成字符串
    valid_str = "".join(valid_list)

    # 把验证码保存在session中，当用户出入验证码发送请求的时候，把用户输入的数据和session中的验证码做对比
    request.session["validcode"] = valid_str
    return HttpResponse(data)


#加减法验证码
def get_validcode_pe():
    img = Image.new(mode="RGB",size=(160,30),color=coderandom())
    draw = ImageDraw.Draw(img,"RGB")
    font_path = os.path.join(BASE_DIR,"static","font","aguzlo.ttf")