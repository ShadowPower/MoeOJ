import datetime


class Helper:
    def get_background_class(self):
        hours = datetime.datetime.now().hour
        if hours >= 19 or hours < 7:
            return 'night'
        elif 7 <= hours < 17:
            return 'day'
        else:
            return 'dusk'
