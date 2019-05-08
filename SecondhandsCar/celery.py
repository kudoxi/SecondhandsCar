from celery import Celery
from django.conf import settings
import os

# 为celery设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SecondhandsCar.settings')

# 创建应用
app = Celery('testcelery')
app.config_from_object('django.conf:settings')
# 酸配置应用
app.conf.update(

    # 本地Redis服务器
    BROKER_URL='redis://176.23.1.213:6379/0',
)

app.autodiscover_tasks(settings.INSTALLED_APPS)

#执行celery -A SecondhandsCar worker --loglevel=DEBUG
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))