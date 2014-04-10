'''
Created on 26 sept. 2013

@author: fclemens
'''
from builtins import print
import logging
import re

from bs4.element import Tag

from engine.urlGenerator import UrlGenerator
from search.Ad import Ad
from utils.parsers.AbstractHTMLParser import AbstractHTMLParser


logger = logging.getLogger(__name__)

class LBCSearchEngine():
    name = "LBC";
    urlGenerator = ""
    '''
    classdocs
    '''
   
    def __init__(self):
        self.urlGenerator = LBCUrlGenerator()
        self.resultsParser = LBCSearchResultsParser()
        print("LBC search engine init ok");
        '''
        Constructor
        ''' 
    
    def search(self, criteria):
        logger.debug("launch '%s' on %s." %  (criteria.name, self.name))
        urls = self.urlGenerator.generate(criteria)
        lstAds = []
        #TODO : improve using threads...
        for url in urls:
            lstAds += self.resultsParser.parse(url);
        
            #Filter on price. LBC use some predefined price, so we have to check with criteria price.
            lstAds = list(filter(lambda ad: ad.price and (ad.price > criteria.prices['min']), lstAds));
            lstAds = list(filter(lambda ad: ad.price and (ad.price < criteria.prices['max']), lstAds));
        
        return lstAds
        #if lstAds:
        #    print("trouve : %i " % len(lstAds))
        #    for ad in lstAds:
        #        print(" \-> %s " % ad.title)
        #else:    
        #    print("rien trouve : ")
        

class LBCUrlGenerator(UrlGenerator):
    '''
    classdocs
    '''
    ARG_TOWN        = "location"
    ARG_PRICE_MIN   = "ps"
    ARG_PRICE_MAX   = "pe"
    ARG_CAT         = "c"
    ARG_DEPARTEMENT = "w"
    ARG_QUERY        = "q"
    
    #TODO : transform in class ?
    #codesCategories={0:"55",1:["9","11"],2:"20",3:"41",4:"23",5:"44",6:"19",7:"6",8:"39",9:"52",10:"16",11:"15"}
    codesCategories={0:"55",1:["9"],2:"20",3:"41",4:"23",5:"44",6:"19",7:"6",8:"39",9:"52",10:"16",11:"15"}
    #codesLBCRegion={"midi_pyrenees":"midi_pyrenees","aquitaine":"aquitaine","languedoc_roussillon":"languedoc_roussillon"}
    #codesLBCDepartement={"31":"131"}
    #soup=BeautifulSoup(urllib.request.urlopen(self.generateURL(search)))
    
    
    def __init__(self):
        super().__init__()
        self.urls=["http://www.leboncoin.fr/annonces/offres/"]
    
    def generateLocations(self, criteria):
        
        if not criteria.locations:
            logger.error("ERROR : no localisation found")
        lstLocations=[]
        for location in criteria.locations:
            if location.type == "town" :
                lstLocations.append(location.parent.parent.code+"/"+location.parent.code+"/?f=a&th=1&"+self.ARG_TOWN+"="+location.name)
                logger.debug("add town : %s" % location.name)
                
        #    if pays['sub']:
        #        for region in pays['sub']:
        ##            if region['sub']:
         #               for departement in region['sub']:
        #                    #codeDepartementInterneLBC = self.codesLBCDepartement.get(departement['code'])
        #                    if departement['sub']:
        #                        for ville in departement['sub']:
        ###                            lstLocations.append(region['code']+"/"+departement['code']+"/?f=a&th=1&"+self.ARG_TOWN+"="+ville['name'])
        #                            logger.debug("add town : %s" % ville['name'])
        #                    else:
        #                        lstLocations.append(region['code']+"/"+departement['code']+"/?f=a&th=1")
        #                        logger.debug("add department : %s" % departement['name'])
        #            else:
        #                lstLocations.append(region['code']+"/?f=a&th=1")
        #                logger.debug("add region : %s" % region['name'])
        #    
        #    else:
        #        #pour rechercher dans tous le pays, il faut tout de m�me entrer une region..........
        #        lstLocations.append("midi_pyrenees/occasions/?f=a&th=1")
        #        logger.debug("add country : %s" % pays['name'])
                
        self.addStringsToUrls(lstLocations)
            
    
    #Parceque la liste de choix des prix evolue sur LBC en fonction de la categorie choisi.
    def getCodesPrice(self, categoryCode, pricesFromCriteria):
        url="http://www.leboncoin.fr/annonces/offres/?"+self.ARG_CAT+"="+categoryCode
        parser = LBCPriceParser();
        return parser.parse(url, pricesFromCriteria['min'], pricesFromCriteria['max'])
        
    
    def generate(self, criteria):
        self.generateLocations(criteria);

        if criteria.query:
            self.addUniqueArg(self.ARG_QUERY, criteria.query.replace(' ','+'))

        #add LBC category codes corresponding to Assa category
        if criteria.categories:
            lstArgs = []
            for cat in criteria.categories:                
                for categoryCode in self.codesCategories.get(cat.id):
                    logger.debug("Get price codes for categoryCode "+categoryCode+".")
                    pricesCodes = self.getCodesPrice(categoryCode, criteria.prices)                
                    lstArgs.append([{'name':self.ARG_CAT,'value':categoryCode},{'name':self.ARG_PRICE_MAX,'value':[pricesCodes['max']]},{'name':self.ARG_PRICE_MIN,'value':pricesCodes['min']}])
            self.addArgsSets(lstArgs)
        return self.urls;


class LBCSearchResultsParser(AbstractHTMLParser):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.adParser = LBCAdParser();

    def parse(self, url):
        logger.debug(" \-> URL %s" % url);
        #print("     \-> Start");
        divAnnonces=self.retrieveOnlinePage(url).find('div',attrs={'class' : 'list-lbc'})
        lstAds=[]
        if divAnnonces:
            for ann in divAnnonces.findAll('a'):
                #print(ann['title'])
                #adParser = LBCAdParser(ann['href'])
                #lstAds.append(adParser.parsePage())
                lstAds.append(self.adParser.parse(ann['href']))

        #print(" \-> End");
        return lstAds
    


class LBCAdParser(AbstractHTMLParser):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def parse(self,url):
        ann=Ad()
        ann.link=url

        #strpage=urllib.request.urlopen(url).read()
        container=self.retrieveOnlinePage(url).find('div',attrs={'class' : 'lbcContainer'})
         

        villeTh=container.find('th',text='Ville :')
        if villeTh:
            villeTR=villeTh.findParents('tr')[0]
            ann.location=villeTR.find('td').find(text=True)

        #Add to postfilter : date et prix car necessite de connaitre la recherche

            ##Car LBC ne recherche que par fourchette de prix. On reverifie donc.
            #if ann.prix and (self.prix['max'] and int(ann.prix) > int(self.prix['max']) or self.prix['min'] and int(ann.prix) < int(self.prix['min'])):


        #Si la ville n'est pas precise dans l'annonce en ligne on prends celle de la recherche
        #if not ann.ville:
        #    ann.ville=self.ville
                        

        ##Date de publication de l'annonce
        #dateAnnonce=container.find('div',attrs={'class' : 'upload_by'})
        #for text in dateAnnonce:
        #    if not isinstance(text,Tag) and not text==' Mise en ligne par ':
        #        ann.date=text.replace(' le ','').replace('.','').replace('� ','').strip()

        #locale.setlocale(locale.LC_ALL,'')
        #ann.date=datetime.strptime(ann.date, '%d %B %H:%M')
        #now = datetime.now()
        #if(ann.date.month>now.month  or (ann.date.month==now.month and ann.date.day>now.day)):
        #    #Cas d'une annonce de l'annee precedente
        #    ann.date=ann.date.replace(year=now.year-1)
        #else:
        #    ann.date=ann.date.replace(year=now.year)

        #if self.dateLimite and time.mktime(ann.date.timetuple())<self.dateLimite:
        #    return;
        
        
        
        
        ##Titre de l'annonce
        titre =container.find('div',attrs={'class' : 'header_adview'})
        if titre:
            h2=titre.find('h2')
            if h2:
                ann.title=h2.find(text=True)
        #print("ann.title"+ann.title)
        
        ##Prix de l'annonce
        price =container.find('span',attrs={'class' : 'price'})
        if price:
            price = re.sub(r'[^\w]', '', price.find(text=True))
            if price :
                ann.price=int(price)


        ##Description de l'annonce
        desc =container.find('div',attrs={'class' : 'content'})
        if desc:
            for text in desc:
                if not isinstance(text,Tag):
                    ann.desc+=text


        ##Images de l'annonce(dans les vignettes d'abord s'il y en a)
        thumbCarroussel=container.find('div',attrs={'id' : 'thumbs_carousel'})
        if(thumbCarroussel):
            for i in thumbCarroussel.findAll('a'):
                styleThumb=i.find('span',attrs={'class' : 'thumbs'})['style']
                styleThumb = styleThumb.replace('background-image: url(\'','')
                styleThumb = styleThumb.replace('\');','')
                urlImage = styleThumb.replace('thumbs','images')
                ann.lstImages.append(urlImage)  
        else:
            image=container.find('div',attrs={'class' : 'images_cadre'})
            if image:
                styleImage=image.find('a')['style']
                styleImage = styleImage.replace('background-image: url(\'','')
                styleImage = styleImage.replace('\');','')
                ann.lstImages.append(styleImage)
        #print("addad")
        return ann


class LBCPriceParser(AbstractHTMLParser):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def parse(self,url, minPrice, maxPrice):
        
        page = self.retrieveOnlinePage(url)
        pricesCodes = {}
        
        #TODO : g�rer cas ou pas de prix select (voir l'options 'locations')
        priceMinSelectBox = page.find('select',attrs={'id' : 'ps'})
        if minPrice and priceMinSelectBox:
            for option in priceMinSelectBox.findAll('option'):
                valeurPrix=option.find(text=True).replace(' ','')
                if(valeurPrix.isdigit() and int(valeurPrix)<=int(minPrice)):
                    pricesCodes["min"]=option['value']
                    
                    
        priceMaxSelectBox=page.find('select',attrs={'id' : 'pe'})
        if maxPrice and priceMaxSelectBox:
            for option in priceMaxSelectBox.findAll('option'):
                pricesCodes["max"] = option['value']
                valeurPrix=option.find(text=True).replace(' ','')
                if(valeurPrix.isdigit() and int(valeurPrix)>=int(maxPrice)):
                    break
                        
        return pricesCodes
      
        