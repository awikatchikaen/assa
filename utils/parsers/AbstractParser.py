'''
Created on 26 sept. 2013

@author: fclemens
'''
import abc
import urllib


class AbstractParser:
    __metaclass__ = abc.ABCMeta
    '''
    classdocs
    '''
    
  
    @abc.abstractmethod
    def parsePage(self):
        """Method documentation"""
        return

    def __init__(self):
        '''
        Constructor
        '''
        print("AbstractParser")
        