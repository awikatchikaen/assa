'''
Created on 26 sept. 2013

@author: fclemens
'''
from utils.parsers.AbstractHTMLParser import AbstractHTMLParser


class LBCSearchEngine():
    '''
    classdocs
    '''
   
    def __init__(self, url):
        '''
        Constructor
        ''' 
    

class LBCUrlGenerator():
    '''
    classdocs
    '''
    #soup=BeautifulSoup(urllib.request.urlopen(self.generateURL(search)))
    
    


class LBCSearchResultsParser(AbstractHTMLParser):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def generateURL(self, search):
        """Method documentation"""
        return "http://free.fr"

    def parsePage(self, search):
        print("LBCSearchResultsParser parsePage")
        divAnnonces=self.retrievePage(search).find('div',attrs={'class' : 'list-lbc'})
        lstAds=[]
        if divAnnonces:
            for ann in divAnnonces.findAll('a'):
                adParser = LBCAdParser(ann['href'])
                lstAds.append(adParser.parsePage())

        return lstAds
    


class LBCAdParser(AbstractHTMLParser):
    '''
    classdocs
    '''


    def __init__(self, url):
        '''
        Constructor
        '''
        