#!/usr/bin/env python
#coding=utf-8
from flask.ext.script import Manager
from app import createApp

app = createApp()
manager = Manager(app)
app.config.from_object(DevConfig)

if __name__ == "__main__":
    manager.run()
