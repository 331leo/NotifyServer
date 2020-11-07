from sanic import Sanic
#Sanic
app = Sanic (__name__)
app.config['JSON_AS_ASCII'] = False

from NotifyServer.server import *

if __name__ == "__main__":
    ssl_context ={"cert":"./cert/fullchain.pem",'key': "./cert/privkey.pem"}
    app.run(host='0.0.0.0',port=443,ssl=ssl_context)