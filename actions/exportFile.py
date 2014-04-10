'''
Created on 4 avr. 2014

@author: fcs
'''
import os


class ExportFile(object):
    '''
    classdocs
    '''


    def __init__(self, exportDirectory):
        '''
        Constructor
        '''
        self.exportDirectory = exportDirectory
        
    def generateFilename(self, name):
        return "ASSA-%s.txt" % (name)
    
    def generateText(self, ad):
        text = "---> %s (%s €)\n" % (ad.title,ad.price)
        text +="  \--> %s\n" % ad.desc.replace('\n',' ')
        text +="  \--> %s\n" % ad.link
        text +="  \--> %s\n" % ad.location

        return text
    
    def execute(self, ad, name):
        f = open(self.exportDirectory+os.sep+self.generateFilename(name),'a',encoding='utf-8')
        f.write(self.generateText(ad))
        f.close()