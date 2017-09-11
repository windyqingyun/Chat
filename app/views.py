#!/usr/bin/env python
#coding=utf-8
from flask import render_template,redirect,request,session,jsonify
from . import app
from .forms import  LoginForm
from .models import  User,Kf,ChatRecord
from .tools import  get_uuid,get_now,get_dict
import json

chatRecords =[]
onlineUsers = {}
onlineKfs = {}

@app.route('/index')
def go():
    return render_template('talk.html')


@app.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        role =  form.role.data
        session['role'] = role

        id = get_uuid()
        if role :
            kf = Kf(id,name)
            onlineKfs[id] = kf

            return render_template('chatKf.html',kf = kf)
        else :
            user = User(id,name)
            onlineUsers[id] = user
            kf = getFreeKf()
            if kf :
                kf.addUser(user)
            return  render_template('chat.html' ,user = user ,kf = kf)



    return render_template('login.html',form=form)

@app.route('/sendMsg',methods=['POST','GET'])
def sendMsg():
    #获取用户的发送信息,保存到数据库中
    fromId = request.form.get('fromId')
    fromName = request.form.get('fromName')
    toId = request.form.get('toId')
    toName = request.form.get('toName')
    content = request.form.get('content')
    date = get_now()

    chatRecord = ChatRecord(fromId,fromName,toId,toName,content,date)

    chatRecords.append(chatRecord)

    return 'success'


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
        kf = onlineKfs.get(id,None)
        if kf and kf.userLen() > 0:
            users = kf.getUsers()
            return jsonify({'message': returnChat,'users':users })

    return jsonify({'message': returnChat })



def getNewRecord(userId):
    #获取最新信息
    for chat in chatRecords:

        if chat.isRead: continue

        if chat.toId == userId:
            chatRecords.remove(chat)
            return  chat

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