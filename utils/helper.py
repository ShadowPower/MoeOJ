import datetime
import time


class Helper:
    @staticmethod
    def get_background_class():
        hours = datetime.datetime.now().hour
        if hours >= 19 or hours < 7:
            return 'night'
        elif 7 <= hours < 17:
            return 'day'
        else:
            return 'dusk'

    @staticmethod
    def get_datetime_str():
        return time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))

    # 获取排除指定参数的GET请求URL，如果个数超过1，末尾自动加&
    @staticmethod
    def get_GETS_except(request, property):
        GETS = {}
        # 转存GET请求的参数，跳过指定参数
        for key in request.GET:
            if key == property:
                continue
            GETS[key] = request.GET[key]
        result = '?' + '&'.join([str(key)+'='+str(GETS[key]) for key in GETS]) + '&'
        return result if len(GETS) > 0 else '?'
