'''
Created on 24 sept. 2013

@author: awikatchikaen
'''

from parsers.LBC.LBCparser import LBCSearchResultsParser
from parsers.ParsersManager import ParsersManager


if __name__ == '__main__':
    print("init assa")
    parserManager = ParsersManager()
    parserManager.registerParser("LBC",LBCSearchResultsParser())
    parserManager.getListParsers()
    pass