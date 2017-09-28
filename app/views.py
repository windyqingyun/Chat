#!/usr/bin/env python
#coding=utf-8
from flask import render_template,redirect,request,session,jsonify,g,make_response
from . import app
from .forms import  LoginForm
from .models import  User,Kf,ChatRecord
from .tools import  get_uuid,get_now,get_dict
import json
from .uploader import Uploader
import os,re

chatRecords =[]
onlineUsers = {}
onlineKfs = {}

@app.route('/talk')
def toTalk():

    id = get_uuid()
    kf = Kf(id, u'客服一')
    onlineKfs[id] = kf
    session['currentUser'] = get_dict(kf)
    session['role'] = True

    return render_template('talk.html', kf=kf)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/kf')
def toKf():
    return render_template('kefu_all.html')

@app.route('/kf/all')
def kfAll():
    return render_template('kefu_all.html')
@app.route('/kf/group')
def kfGroup():
    return render_template('kefu_group.html')

@app.route('/kf/add')
def kfAdd():
    return render_template('kefu_add.html')


@app.route('/user')
def toUser():
    return render_template('user.html')

@app.route('/password')
def toPassword():
    return render_template('password.html')

@app.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        name = form.name.data
        id = get_uuid()

        session['role'] = False
        user = User(id,name)
        session['currentUser'] = get_dict(user)

        onlineUsers[id] = user
        kf = getFreeKf()

        if kf :

            kf.addUser(user)
        return  render_template('chat.html' ,user = user ,kf = kf)



    return render_template('login.html',form=form)

@app.route('/sendMsg',methods=['POST','GET'])
def sendMsg():
    #获取用户的发送信息,保存到数据库中
    kfId = request.form.get('kfId')
    kfName = request.form.get('kfName')
    userId = request.form.get('userId')
    userName = request.form.get('userName')
    fromFlag = request.form.get('fromFlag')
    content = request.form.get('content')
    date = get_now()

    chatRecord = ChatRecord(kfId,kfName,userId,userName,fromFlag,content,date)
    chatRecords.append(chatRecord)

    return 'success'

@app.route('/getMsg',methods=['POST','GET'])
def getMsg():

    kfId = request.form.get('kfId')
    userId = request.form.get('userId')

    returnRecords = getAllChatRecord(kfId,userId)

    return jsonify({'message': returnRecords })


@app.route('/getReply',methods=['POST','GET'])
def getReply():
    #从数据库中查询自己最新的回复

    id =  request.form.get('id')
    chatRecord = getNewRecord(id)
    returnChat = ''

    if chatRecord:
        chatRecord.read()
        chatRecords.append(chatRecord)
        returnChat = get_dict(chatRecord)

    role = session.get('role')
    print  id
    if role :

        kf = onlineKfs.get(id,None)
        print kf
        if kf and kf.userLen() > 0:
            users = kf.getUsers()
            return jsonify({'message': returnChat,'users':users })

    return jsonify({'message': returnChat })

def getAllChatRecord(kfId,userId):
    returnRecords = []
    for chat in chatRecords:
        if chat.kfId == kfId and chat.userId == userId:
            returnRecords.append(get_dict(chat))
    return returnRecords

def getNewRecord(userId):
    returnRecord = None
    #获取最新信息
    for chat in chatRecords:
        if chat.isRead: continue
        if session['role']:
            if chat.kfId == userId and chat.fromFlag == 'u':
                returnRecord = chat
                break
        else:
            if chat.userId == userId and chat.fromFlag == 'k' :
                returnRecord = chat
                break

    if returnRecord:
        chatRecords.remove(returnRecord)
    return  returnRecord

def getFreeKf():
    #获取空闲客服
    min = 10
    returnKf = None

    for key in onlineKfs:
        value = onlineKfs.get(key)
        num = value.userLen()
        if num < min :
            min = num
            returnKf = value

    return returnKf

#参考来自:https://coding.net/u/wtx358/p/flask-ueditor-demo/git/tree/master
@app.route('/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口
    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
    action = request.args.get('action')
    print action
    # 解析JSON格式的配置文件
    with open(os.path.join(app.static_folder, 'ueditor', 'jsp',
                           'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}
    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG
    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }
        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, app.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, app.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']
        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)
        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, app.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })
        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list
    else:
        result['state'] = '请求地址出错'
    result = json.dumps(result)
    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})
    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res