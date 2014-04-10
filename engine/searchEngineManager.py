'''
Created on 26 sept. 2013

@author: fclemens
'''
import logging


logger = logging.getLogger(__name__)

#TOPO add deactivateEngine (si le site change de pr�sentation)
class SearchEngineManager(object):
    '''
    classdocs
    '''
    lstSearchEngines =[];

    def registerSearchEngine(self, engine):
        if not engine.name in self.lstSearchEngines:
            self.lstSearchEngines[engine.name] = engine
            logger.info("register new searchEngine : %s" %  engine.name);



    def getListSearchEngine(self):
        return self.lstSearchEngines
        #for parserName in self.lstSearchEngines.keys():
            #print("%s;" % parserName)
            
     

    def __init__(self):
        '''
        Constructor
        '''
        self.lstSearchEngines = {}
        