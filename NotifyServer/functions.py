import asyncio
import datetime
from urllib3.util import parse_url
# zoommtg://zoom.us/join?action=join&confno=98770497040&pwd=a2trcllPclVpRmQrYTJ6R1ZOWGIrdz09
# https://zoom.us/j/98770497040?pwd=a2trcllPclVpRmQrYTJ6R1ZOWGIrdz09#success


async def get_processed_data(odata,db,index=None):
    school_name = odata['school']
    class_name = odata['class']
    period=0
    if index:
        period = index
    elif odata.get("index",None):
        period = int(odata.get("index"))
    else:
        #period = whattime()
        t = datetime.datetime.now()
        now = f"{str(t.hour) if len(str(t.hour)) == 2 else '0'+str(t.hour)}:{str(t.minute) if len(str(t.minute)) == 2 else '0'+str(t.minute)}"
        try:
            timers = db['school'].get(school_name,{}).get(class_name.split("-")[0],{}).get('timers',None) if db['school'].get(school_name,{}).get(class_name.split("-")[0],{}).get('timers',None) else db['default']['timers']
        except Exception as e:
            timers = db['default'].get("timers")
            print(f"디폴트타이머 사유: {e}")
        print(timers)
        for timer in timers:
            if timer >= now:
                period = timers.index(timer)
                break
    
    try:
        nowdb=db['school'][school_name][class_name][datetime.datetime.now().weekday()][period]
    except:
        return None
    try:
        if "zoom.us/j" in str(nowdb['url']):
            basezoom = "zoommtg://zoom.us/join?action=join&confno="
            basezoom += parse_url(nowdb['url']).path.split("/")[2] + "&" + parse_url(nowdb['url']).query
            nowdb.update({"url":basezoom.replace("%20","").replace("%0A","")})

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