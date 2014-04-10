'''
Created on 10 avr. 2014

@author: fcs
'''
import ast


class Actionnable(object):
    '''
    classdocs
    '''


    def configure(self, params):
        '''
        Constructor
        '''
        if params:
            for cle, valeur in ast.literal_eval(params).items():
                setattr(self, cle, valeur)