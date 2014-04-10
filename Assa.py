'''
Created on 24 sept. 2013

@author: awikatchikaen
'''

from datetime import datetime
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from actions.exportFile import ExportFile
from actions.mail import Mailer
from actions.pushover import Pushover
from database import Base
import database
from engine.LBC.LeBonCoin import LBCSearchEngine
from engine.searchEngineManager import SearchEngineManager


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
#http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python

if __name__ == '__main__':
    #TODO : add auto discover SEM
    searchEngineManager = SearchEngineManager()
    searchEngineManager.registerSearchEngine(LBCSearchEngine())
    searchEngineManager.getListSearchEngine()
    
    #TESTS
    #generator = UrlGenerator()
    #generator.addArgsSets([[{'name':'arg1','value':'1'},{'name':'arg2','value':['2.1','2.2']},{'name':'arg3','value':'3'}],[{'name':'arg1','value':'10'},{'name':'arg2','value':['20.1','20.2']},{'name':'arg3','value':'30'}]])
     
    engine = create_engine('sqlite:///C:\Windows\Temp\sqlalchemy_example.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    lstSearch = session.query(database.Criteria).all()
    
    
    #action = Mailer('smtp.gmail.com', 587)
    #action = ExportFile('C:\Windows\Temp')
    
    Mailer.smtpServer = 'smtp.gmail.com'
    Mailer.smtpPort = 587
    
    
    
    for c in lstSearch:
        for engine in c.sites: 
            lstAds = []
            if not engine.name in searchEngineManager.getListSearchEngine():   
                logger.error("engine not exist : %s." %  engine.name )
            else:
                engine = searchEngineManager.getListSearchEngine()[ engine.name]
                lstAds += engine.search(c)
                
            if lstAds:
                print("trouve : %i " % len(lstAds))
                for ad in lstAds:
                    print(" \-> %s " % ad.title)
                    constructor = globals()[c.action.type]
                    action = constructor()
                    action.configure(c.action.config)
                    action.execute(ad, c.name)
                    
            else:    
                print("rien trouve : ")
    
    
    pass