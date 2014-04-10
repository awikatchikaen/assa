'''
Created on 1 avr. 2014

@author: fcs
'''
import copy

from pkg_resources import basestring


class UrlGenerator(object):
    '''
    classdocs
    '''
    def __init__(self):
        self.page=""
        self.urls = []
    
    def __addTextToList__(self, list, text):
        newList = []
        for string in list:
            newList.append(string+ text)
        return newList
    
    def addStringsToUrls(self, values):
        #if not arg:
        #    print("Argument non defini pour ce parser : "+arg)
        if values:
            if isinstance(values, basestring):
                #TODO :check if last char is diffrent of /
                self.urls = self.__addTextToList__(self.urls, values)
            else:
                orginalUrls = list(self.urls)
                self.urls = []
                for value in values:
                    self.urls += self.__addTextToList__(orginalUrls, value)
    
    def addUniqueArg(self, arg, values):
        #if not arg:
        #    print("Argument non defini pour ce parser : "+arg)
        if values:
            if isinstance(values, basestring):
                #TODO :check if last char is diffrent of /
                self.urls = self.__addTextToList__(self.urls, "&"+arg+"="+values)
            else:
                orginalUrls = list(self.urls)
                self.urls = []
                for value in values:
                    self.urls += self.__addTextToList__(orginalUrls, "&"+arg+"="+value)
    
    
    def __addOneSetOfArgs__(self, args):
        textsForSet = ['']
        for arg in args:
            if arg['value']:
                if isinstance(arg['value'], basestring):
                    #TODO :check if last char is diffrent of /
                    textsForSet = self.__addTextToList__(textsForSet,"&"+arg['name']+"="+arg['value'])
                else:
                    originalTexts = list(textsForSet)
                    textsForSet = []
                    for value in arg['value']:
                        textsForSet += self.__addTextToList__(originalTexts, "&"+arg['name']+"="+value)     
        return textsForSet
    
        
    
    def addArgsSets(self, argsSets):
        if argsSets:
            textToAdd = []
            for argsList in argsSets:
                textToAdd += self.__addOneSetOfArgs__(argsList)
            
            self.addStringsToUrls(textToAdd)

     
            

        