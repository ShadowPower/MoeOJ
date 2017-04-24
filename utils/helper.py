import datetime, time, math


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

    # 将类似于 A B C D 的序号转成 0 1 2 3
    @staticmethod
    def order_abc_to_123(order):
        result = 0
        temp = order.upper()[::-1]
        for i, c in enumerate(temp):
            if i > 0:
                result += (ord(c) - 64) * 26**i
            else:
                result += ord(c) - 65
        return result

    # 将类似于 0 1 2 3 的序号转成 A B C D
    @staticmethod
    def order_123_to_abc(order):
        # 当前剩余的数字
        temp = int(order) + 1
        result = []
        # 求得位数
        temp2 = 0
        digit = 0
        while temp > temp2 * 26 + 26:
            digit += 1
            temp2 = temp2 * 26 + 26
        temp -= temp2 + 1
        # 转成字母
        while digit >= 0:
            result.append(chr(temp % 26 + 65))
            temp //= 26
            digit -= 1
        return ''.join(result[::-1])
