import os
import web
import json
import datetime
import time
import memcache

mc = memcache.Client()

urls = (
    '/', 'Hello',
    '/str','stroage',
    '/getdata','data',
    '/favicon.ico', 'StaticFile'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

mc = memcache.Client()
#mc.set("WWAVG", '{"lowtemp": [28.4, 28.4, 27.75, 27.5, 24.25, 21.75, 22.0, 22.0, 22.0, 23.5, 23.75, 23.5, 25.5, 26.75, 25.5, 27.25, 28.0, 28.25, 28.75, 29.75], "lowtick": [1466434800.0, 1466443800.0, 1466553600.0, 1466695800.0, 1466771400.0, 1466816400.0, 1466899200.0, 1466969400.0, 1467064800.0, 1467153000.0, 1467298800.0, 1467318600.0, 1467410400.0, 1467498600.0, 1467579600.0, 1467669600.0, 1467752400.0, 1467842400.0, 1467923400.0, 1468020600.0], "avg": [28.72, 30.85, 30.11, 31.53, 25.69, 22.96, 23.59, 22.85, 24.36, 26.91, 25.27, 25.59, 27.15, 28.13, 28.22, 29.07, 29.53, 30.08, 32.08, 32.74], "hightemp": [29.1, 35.4, 34.0, 40.25, 28.25, 24.75, 25.75, 23.75, 27.5, 33.75, 27.0, 29.0, 32.0, 34.0, 34.5, 32.75, 33.25, 33.5, 39.0, 38.0], "hightick": [1466407620.0, 1466487000.0, 1466573400.0, 1466661600.0, 1466717400.0, 1466784000.0, 1466915400.0, 1467018000.0, 1467102600.0, 1467180000.0, 1467216000.0, 1467343800.0, 1467441000.0, 1467525600.0, 1467613800.0, 1467702000.0, 1467783000.0, 1467871200.0, 1467957600.0, 1468045800.0]}')

class StaticFile:

    def GET(self):
        if not self.cache_valid(os.path.join(app_root, 'favicon.ico')):
            with open(os.path.join(app_root, 'favicon.ico'), 'rb') as ico:
                return ico.readall()

    def cache_valid(path):
        return False
        last_time_str = web.ctx.env.get('HTTP_IF_MODIFIED_SINCE', '')
        last_time = web.net.parsehttpdate(last_time_str)

        if last_time:
            mtime = os.path.getmtime(path)
            if last_time < mtime:
                web.notmodified()
                return True
        web.lastmodified(datetime.datetime.now())
        return False


class data:

    def cache_valid(self):
        #return False
        last_time_str = web.ctx.env.get('HTTP_IF_MODIFIED_SINCE', '')
        last_time = web.net.parsehttpdate(last_time_str)

        if last_time:
            nowtick = int(time.time())
            tick = time.mktime(last_time.timetuple())
            nexttick = tick+(300-tick % 300)
            #print "weiwei"+datetime.datetime.fromtimestamp(nexttick).strftime("%m-%d %H %M %S")
            if nexttick > nowtick:
                web.notmodified()
                return True
        web.lastmodified(datetime.datetime.now())
        return False

    def GET(self):
        if not self.cache_valid():
            input = web.input()
            for key in input:
                    return json.dumps(mc.get(key))


    def POST(self):
        dic = eval(web.data())
        if dic['user'] == 'liwei33333':
            for key in dic:
                if key != "user":
                    mc.set(key, dic[key])
            return 'o'
        return 'b'


class Hello:
    def GET(self):
        return render.index()


web.config.debug = True
app = web.application(urls, globals()).wsgifunc()


