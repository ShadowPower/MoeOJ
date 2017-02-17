from OJ.helper import Helper

def day_night_change(request):
    return {'background_class': Helper.get_background_class()}

def server_time(request):
    return {'server_time': Helper.get_datetime_str()}