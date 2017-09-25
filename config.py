class Config(object):
    '''Base config class.'''
    SECRET_KEY = 'you try'
    JSON_AS_ASCII = 'FALSE'

class ProdConfig(Config):
        '''Production config class.'''

class DevConfig(Config):
        '''Development config class. '''
        #Open the DEBUG
        DEBUG = True
        #DEBUG = False
   
