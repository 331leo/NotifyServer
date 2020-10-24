import datetime

import flask
import openpyxl
from flask import Flask, request, jsonify,redirect
from flask_cors import CORS
import ssl
import time
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
import random

try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate('etc/leobot-9fbb1-firebase-adminsdk-p6m4j-ff50753b80.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://leobot-9fbb1.firebaseio.com/'
    })

#sms
api_key = "NCSUFQVQAJOTSP2Y"
api_secret = "US5IDCW3PTIVSMS6ZWNXHKOGCWGOYI0I"
params = dict()
params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
params['from'] = '07079187919'  # Sender number
cool = Message(api_key, api_secret)
app = Flask (__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/botapi')
def botapi():
    fs = open("etc/servercount", 'r')
    fu = open("etc/usercount", 'r')
    ft = open("etc/timecount", 'r')
    fa = open("etc/autocovucount", 'r')
    user = fu.read()
    server = fs.read()
    time = ft.read()
    autocovc = fa.read()
    fu.close()
    fs.close()
    ft.close()
    fa.close()
    return jsonify({"user":user,"server":server,"time":time,"autocovc":autocovc})


@app.route('/autocovphone', methods = ['POST'])
def autocovphone():
    data = request.form
    rdata = data['pn']
    ccode=""
    for r in range(5):
        ccode += str(random.randrange(1, 9))
    try:
        data = rdata.replace(" ","-")
        dir = db.reference(f"webautocheck/{data}")
        data = dir.get()
        pn = data['phonenum']
        name = data['studentName']
        dir.update({"ccode":f"{ccode}"})
        params['to'] = pn  # Recipients Number '01000000000,01000000001'
        params['text'] = f'[Leok.kr] 자동 자가진단 해제 인증번호: {ccode}'  # Message
        try:
            response = cool.send(params)
        except CoolsmsException as e:
            return redirect(f"https://cov.leok.kr/?code=unregpn", code=302) #없는번호
    except Exception as e:
        print (e)
        return redirect(f"https://cov.leok.kr/?code=unrege", code=302) #미등록 유저

    return redirect(f"https://cov.leok.kr/?code=unregc&name={rdata}", code=302) #인증번호 보내기 성공


@app.route('/chk', methods = ['POST'])
def chk():
    data = request.form
    rdata = data['rdata']
    ccode = data['ccode']
    try:
        data = rdata.replace(" ","-")
        dir = db.reference(f"webautocheck/{data}")
        data = dir.get()
        rccode = data['ccode']
        pn = data['phonenum']
        if ccode == rccode:
            dir.delete()
            return redirect(f"https://cov.leok.kr/?code=unregs", code=302) #등록 해제 성공
    except Exception as e:
        print(e)

    return redirect(f"https://cov.leok.kr/?code=unregce&name={rdata}", code=302) #시도 했지만 틀림


@app.route('/autocovidreg', methods = ['POST'])
def autocovidreg():
    data = request.form
    region = data['region']
    level = data['level']
    name = data['schoolname']
    studentName = data['name']
    birthday = data['birthday']
    phonenum = data['phonenumber']

    dir = db.reference(f"webautocheck/{birthday}-{studentName}")
    kk = dir.get()
    print(kk)
    if len(str(kk)) < 10:
        f = open("autocheck/config_o.json", 'rt', encoding='CP949')
        x = f.read()
        f.close()
        x = x.replace("wldur", region)
        x = x.replace("chwndrh", level)
        x = x.replace("gkrrydlfma", name)
        x = x.replace("tkfkadlfma", studentName)
        x = x.replace("toddlf", birthday)
        f = open("autocheck/config.json", 'w')
        f.write(x)
        f.close()
        os.system("cd autocheck; yarn start")

        time.sleep(1)

        f = open("etc/autocheckrc.txt", 'r')
        x = f.read()
        f.close()
        if not x == "6":
            send = ""
            if x == "1":
                return redirect("https://cov.leok.kr/?code=e2", code=302) #학생에러
            if x == "0":
                return redirect("https://cov.leok.kr/?code=e1", code=302) #학교에러
            elif x == "2" or x == "3" or x == "4" or x == "5":
                send = "에러, 구조 확인요청. 개발자에게 문의하세요"

            return
        else:
            dir.update({"region": f"{region}"})
            dir.update({"level": f"{level}"})
            dir.update({"name": f"{name}"})
            dir.update({"studentName": f"{studentName}"})
            dir.update({"birthday": f"{birthday}"})
            dir.update({"phonenum": f"{phonenum}"})
            dir = db.reference(f"webautocheck/")
            p = len(dir.get())
            fa = open("etc/autocovucount", 'w')
            fa.write(str(p))
            fa.close()
            return redirect("https://cov.leok.kr/?code=s", code=302)

    if len(str(kk)) > 10:
        return redirect("https://cov.leok.kr/?code=regd", code=302)

@app.route('/sugphone', methods = ['POST'])
def sugphone():
    data = request.form
    rdata = data['ucode']
    ccode=""
    for r in range(5):
        ccode += str(random.randrange(1, 9))
    try:
        if rdata == '1':
            pn = '01021400443'
        if rdata == '2':
            pn = '01029857442'
        if rdata == '3':
            pn = ''
        dir = db.reference(f"suggest")
        dir.update({"ccode":f"{ccode}"})
        params['to'] = pn  # Recipients Number '01000000000,01000000001'
        params['text'] = f'[신사중 정보부] 신사중 건의함 건의사항 보기 인증번호: {ccode}'  # Message
        try:
            response = cool.send(params)
        except CoolsmsException as e:
            return redirect(f"https://suggest.leok.kr/?code=unregpn", code=302) #없는번호
    except Exception as e:
        print (e)
        return redirect(f"https://suggest.leok.kr/?code=unrege", code=302) #미등록 유저

    return redirect(f"https://suggest.leok.kr/?code=phoneok", code=302) #인증번호 보내기 성공

@app.route('/schk',methods = ['POST'])
def schk():
    data = request.form
    ccode = data['ccode']
    try:
        dir = db.reference(f"suggest/")
        data = dir.get()
        rccode = data['ccode']
        if ccode == rccode:
            fname = f"./etc/apisuggest.xlsx"
            return flask.send_file(fname,attachment_filename="SuggestResult.xlsx", as_attachment=True) #성공
    except Exception as e:
        print(e)

    return redirect(f"https://suggest.leok.kr/?code=wrongcode", code=302)  # 시도 했지만 틀림



@app.route('/simg')
def sugimg():
    fname = request.args.get('name')
    fname = f"./img/{fname}"
    return flask.send_file(fname, mimetype='image')

@app.route('/suggest', methods = ['POST'])
def suggest():    
    data = request.form
    print(data)
    studentnum = data['studentnum']
    studentname = data['studentname']
    cont = data['cont']
    c=str(datetime.datetime.now())[-4:]
    f = request.files['imagefile']

    f.save(f"./img/{studentnum}_{c}_{f.filename}")
    fname = f"{studentnum}_{c}_{f.filename}"

    file = openpyxl.load_workbook("etc/apisuggest.xlsx")
    sheet = file.active
    from urllib import parse
    keyword = fname
    keyword = parse.quote(keyword)
    url = f'https://api.leok.kr/simg?name={keyword}'
    for i in range(1, 500):
        if sheet["A" + str(i)].value == "-":
            sheet["A" + str(i)].value = studentnum
            sheet["B" + str(i)].value = studentname
            sheet["C" + str(i)].value = str(datetime.datetime.now())[:19]
           
            sheet["D" + str(i)].value = f'=HYPERLINK("{url}","{fname}")'
            
            sheet["E" + str(i)].value = cont
            sheet["F" + str(i)].value = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            break
    file.save("etc/apisuggest.xlsx")

    return redirect("https://suggest.leok.kr/?code=s", code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=443,ssl_context=("./cert/fullchain.pem","./cert/privkey.pem"))
