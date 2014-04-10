'''
Created on 4 avr. 2014

@author: fcs
'''

from pushover import PushoverClient
from actions.Actionnable import Actionnable


class Pushover(Actionnable):
    '''
    classdocs
    '''
    smtpServer = ""
    smtpPort = ""

    def __init__(self):
        '''
        Constructor
        '''
        self.mailadress = ""
        
    def generateMailTitle(self, name, ad):
        return "[ASSA][%s][%s] %s  " % (name,ad.location, ad.title)
    
    def generateMailText(self, ad):
        mailText="<html>"
        mailText+="<head>"
        mailText+="<style>"
        mailText+="body {font: 12pt Arial;} "
        mailText+="a:link {font: 12pt Arial; font-weight: bold; color:#0000cc}"
    #    str+="#entry {border: solid 4px #c3d9ff; } "
    #    str+="#body { margin-left: 5px; margin-right: 5px; }//-->"
        mailText+="</style></head>"
        mailText+="<body>"
        if ad.location:
            mailText+="<h2><a href=\'%s\'>%s : %s (%s)</a></h2>" % (ad.link,ad.location, ad.title, ad.price)
        else:
            mailText+="<h2><a href=\'%s\'>%s (%s)</a></h2>" % (ad.link, ad.title, ad.price)
             
            #str+="<span id=\'entry\'>%s</span><br/>" % self.desc
        mailText+="<span>%s</span><br/>" % ad.desc.replace('\n','<br/>')
        for i in ad.lstImages:
            mailText+="<img src=\'%s\'/><br/>" % i
        mailText+="</body></html>"
        
    def execute(self, ad, name):
  
        po = PushoverClient("pushover.config")
        po.send_message("Hello, World : !"+name)
        