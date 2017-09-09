from .tools import get_dict

class User():
    def __init__(self,id,name):
        self.id = id
        self.name = name


class Kf():

    def __init__(self,id,name):
        self.id = id
        self.name = name
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
    def __init__(self,fromId,fromName,toId,toName,content,date):

        self.fromId = fromId
        self.fromName = fromName
        self.toId = toId
        self.toName = toName
        self.content = content
        self.date = date
        self.isRead = False

    def read(self):
        self.isRead = True
