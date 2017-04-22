from utils.helper import Helper
from django.conf import settings

def day_night_change(request):
    return {'background_class': Helper.get_background_class()}

def server_time(request):
    return {'server_time': Helper.get_datetime_str()}

def public_parameter(request):
    return {'oj_title': getattr(settings, 'OJ_TITLE', 'Moe Online Judge')}

# gets_no_page是get参数列表排除page后的文本
def gets_no_page(request):
    return {'gets_no_page': Helper.get_GETS_except(request, 'page')}