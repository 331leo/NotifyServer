import asyncio
import datetime
from urllib3.util import parse_url
# zoommtg://zoom.us/join?action=join&confno=98770497040&pwd=a2trcllPclVpRmQrYTJ6R1ZOWGIrdz09
# https://zoom.us/j/98770497040?pwd=a2trcllPclVpRmQrYTJ6R1ZOWGIrdz09#success


async def get_processed_data(odata,db,index=None):
    school_name = odata['school']
    class_name = odata['class']
    if index:
        period = index
    else:
        period = whattime()
    try:
        nowdb=db['school'][school_name][class_name][datetime.datetime.now().weekday()][period]
    except:
        return None
    try:
        if "zoom.us/j" in str(nowdb['url']):
            basezoom = "zoommtg://zoom.us/join?action=join&confno="
            basezoom += parse_url(nowdb['url']).path.split("/")[2] + "&" + parse_url(nowdb['url']).query
            nowdb.update({"url":basezoom.replace("%20","")})

    except:
        pass
    return nowdb

async def post_data(odata,db):
    school_name = odata['school']
    class_name = odata['class']
    data = odata['data']
    timers = odata.get("timers",None)
    print(db)
    try:
        try:
            db['school'][school_name]
        except:
            db['school'].update({f'{school_name}':{}})
        try:
            db['school'][school_name][class_name].update(data)
            db['school'][school_name][class_name.split("-")[0]].update({"timers":timers})
        except:
            db['school'][school_name] = dict()
            db['school'][school_name].update({f"{class_name}":data})
            db['school'][school_name].update({class_name.split("-")[0]:{"timers":timers}})

        #nowdb=db['school'][school_name][class_name][datetime.datetime.now().weekday()][period]
    except Exception as e:
        print(e)
        return None
    return db

async def get_all_data(odata,db):
    school_name = odata['school']
    class_name = odata['class']
    try:
        nowdb=db['school'][school_name][class_name]
    except Exception as e:
        return None
    return nowdb
async def get_timers(odata,db):
    school_name = odata['school']
    try:
        timers = odata['timers']
        return timers
    except:
        try:
            timers=db['school'][school_name]['timers']
        except Exception as e:
            timers = db['defalut']['timers']
        return timers

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
    elif hour == 13 and min <= 30 or hour == 12:
        return 4
    elif hour == 13 and min > 30:
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