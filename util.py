import asyncio
import datetime
# zoommtg://zoom.us/join?action=join&confno=98770497040&pwd=a2trcllPclVpRmQrYTJ6R1ZOWGIrdz09
# https://zoom.us/j/98770497040?pwd=a2trcllPclVpRmQrYTJ6R1ZOWGIrdz09#success
async def process_data(odata,db):
    school_name = odata['school']
    class_name = odata['class']
    period = whattime()
    try:
        db['school'][school_name][class_name][datetime.datetime.now().weekday()][period]
    except:
        return None


def whattime():
    hour = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    if hour == 8:
        return 0
    elif hour == 9:
        return 1
    elif hour == 10:
        return 2
    elif hour == 11:
        return 3
    elif hour == 13 and min <= 10 or hour == 12:
        return 4
    elif hour == 13 and min > 10:
        return 5
    elif hour == 14 and min <= 30:
        return 5
    elif hour == 14 and min > 30:
        return 6
    elif hour == 15:
        return 6
    else:
        return 0

print(whattime())