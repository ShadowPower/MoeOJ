import datetime


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
