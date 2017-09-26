from .tools import get_dict
import  pymongo
from bson import ObjectId

#conn = pymongo.Connection('localhost', 27017)

#db = conn.chat

class User():
    user = None
    def __init__(self,id,name):
        self.id = id
        self.name = name


    def save(self):
       return self.user.insert(get_dict(self))

    def find(cls,id):
        return cls.user.find_one({"_id":ObjectId(id)})



class Kf():

    kf = None

    def __init__(self,id,name):
        self.name = name
        self.id = id
        self.status = True
        self.users = []

    def changeStatus(self):
        if self.status :
            self.status = False
        else:
            self.status = True



    def isOnline(self):
        return self.status
    
    def addUser(self,user):
        self.users.append(user)

    def userLen(self):
        return len(self.users)

    def getUsers(self):
        users = []
        for user in self.users:
            u = get_dict(user)
            users.append(u)
        return users

class ChatRecord():
    def __init__(self,kfId,kfName,userId,userName,fromFlag,content,date):

        self.kfId = kfId
        self.kfName = kfName
        self.userId = userId
        self.userName = userName
        self.fromFlag = fromFlag
        self.content = content
        self.date = date
        self.isRead = False

    def read(self):
        self.isRead = True
