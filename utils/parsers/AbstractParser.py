'''
Created on 26 sept. 2013

@author: fclemens
'''
import abc
import urllib.request

from bs4 import BeautifulSoup


class AbstractParser:
    __metaclass__ = abc.ABCMeta
    '''
    classdocs
    '''
    
    def  retrieveOnlinePage(self, url):
        #TODO : improve using urllib3 or Requests which have a pool of connection.
        #Permit to avoid open several HTTP connection for same site
        
        pageTelecharge=urllib.request.urlopen(url)
        #pageTelecharge = requests.get(url)
        return BeautifulSoup(pageTelecharge.read())
  
    @abc.abstractmethod
    def parse(self):
        """Method documentation"""
        return

    def __init__(self):
        '''
        Constructor
        '''
        print("AbstractParser")
        