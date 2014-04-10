'''
Created on 4 avr. 2014

@author: fcs
'''
from email.charset import Charset
from email.generator import Generator
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import StringIO
import smtplib

from actions.Actionnable import Actionnable


class Mailer(Actionnable):
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
  
        from_address = [u'Cerebro', 'awikatchikaen@clemens.mobi']
        recipient = [u'Those #!@', self.mailadress]
        
        # Example body
        #html = u'Unicode.\nTest.'
        #text = u'Unicode.\nTest.'
        # Default encoding mode set to Quoted Printable. Acts globally!
        #Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
        # 'alternative. MIME type . HTML and plain text bundled in one e-mail message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "%s" % Header(self.generateMailTitle(name, ad), 'utf-8')
        # Only descriptive part of recipient and sender shall be encoded, not the email address
        msg['From'] = "\"%s\" <%s>" % (Header(from_address[0], 'utf-8'), from_address[1])
        msg['To'] = "\"%s\" <%s>" % (Header(recipient[0], 'utf-8'), recipient[1])
        # Attach both parts
        htmlpart = MIMEText(self.generateMailText(ad), 'html', 'UTF-8')
    #    textpart = MIMEText(str, 'plain', 'UTF-8')
        msg.attach(htmlpart)
    #    msg.attach(textpart)
        # Create a generator and flatten message object to 'file.
        str_io = StringIO()
        g = Generator(str_io, False)
        g.flatten(msg)


        s = smtplib.SMTP(self.smtpServer, self.smtpPort)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("lord.awikatchikaen", "")    
    
        
        s.sendmail("lord.awikatchikaen@gmail.com", recipient[1], str_io.getvalue())