'''
Created on 26 sept. 2013

@author: fclemens
'''
import abc
import urllib

#from bs4 import BeautifulSoup

from utils.parsers.AbstractParser import AbstractParser


class AbstractHTMLParser(AbstractParser):
    __metaclass__ = abc.ABCMeta
    '''
    classdocs
    '''
     

        
    def __init__(self):
        '''
        Constructor
        '''
        print("AbstractHTMLParser")
        