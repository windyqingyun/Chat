#!/usr/bin/env python
#coding=utf-8
from flask_script import Manager
from config import DevConfig
from app import createApp

app = createApp()
manager = Manager(app)
app.config.from_object(DevConfig)


if __name__ == "__main__":
    manager.run()
