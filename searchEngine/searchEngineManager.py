'''
Created on 26 sept. 2013

@author: fclemens
'''


class ParsersManager(object):
    '''
    classdocs
    '''

    def registerSearchEngine(self, parserName, parser):
        self.lstSearchEngines[parserName] = parser
        print("register new searchEngine :"+parserName);



    def getListSearchEngine(self):
        for parserName in self.lstSearchEngines.keys():
            print("%s" % parserName)
            
     

    def __init__(self):
        '''
        Constructor
        '''
        self.lstSearchEngines = {}
        