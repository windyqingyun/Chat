#!/usr/bin/env python
#coding=utf-8
from flask import  Flask
#from flask_bootstrap import  Bootstrap
app = Flask(__name__)

def createApp():
    app.config['SECRET_KEY'] = 'asd'
#    bootstrap = Bootstrap(app)

    return app


from . import  views,forms,models,tools,uploader