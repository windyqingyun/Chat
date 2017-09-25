#!/usr/bin/env python
#coding=utf-8
from flask import render_template,redirect,request,session,jsonify,g
from . import app
from .forms import  LoginForm
from .models import  User,Kf,ChatRecord
from .tools import  get_uuid,get_now,get_dict
import json

chatRecords =[]
onlineUsers = {}
onlineKfs = {}

@app.route('/talk')
def go():

    id = get_uuid()
    kf = Kf(id, u'客服一')
    onlineKfs[id] = kf
    session['currentUser'] = get_dict(kf)
    session['role'] = True

    return render_template('talk.html', kf=kf)

@app.route('/kf')
def toKf():
    return render_template('test.html')

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

    if role :
        print id
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