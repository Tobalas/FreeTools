# -*- coding: utf-8 -*-
'''
Created on 11 de jun de 2019
@author: Tobias Rocha <tobiasramosrocha@gmail.com>
@license: GPL
@requires: scipy
@url: https://github.com/Tobalas/FreeTools/
@usage:
from BlackSholes import Formula
bs = Formula(So, X, sigma, r, q, t)
bs.defineCallPut()
delta = 0.00
rho = 0.00
option_value = 0.00
if CALCULATED_OPTION_IS_A_CALL:
    delta = bs.deltaCall()
    option_value = bs.CALL
    rho = bs.rhoCall()
else:
    delta = bs.deltaPut()
    option_value = bs.PUT
    rho = bs.rhoPut()
gamma = bs.gamma()
vega = bs.vega()


'''
import math

from scipy.stats import norm

GREEKS_PRECISION = 2

class Formula():
    def __init__(self,So,X,sigma,r,q,t,year_size=365):
        """Instantiates a class Formula to calculate stock options prices

        Args:
            So (float): The price of the referenced asset
            X (float): The price of option strike
            sigma (float): The derivated asset volatility
            r (float): Risk-less interest tax
            q (float): Divident yield
            t (int): Days until the option expires
            year_size (int): Default size of year (365 days). For work days only use 255 or you need a work day calendar for the country of risk-less tax
        """
        self.So = So # ASSET PRICE
        self.X = X # STRIKE
        self.sigma = sigma/100 # ASSET VOLATILIRY
        self.r = r/100 # selic 
        self.q = q/100 #dividend yeld
        self.t = self.porcentagemAno(t,year_size) /100  # tempo até o vencimento em dias
        
        self.CALL = False # call value
        self.PUT = False # put value
        
        self.d1 = 0
        self.d2 = 0
    
    def N(self,x):
        return norm.cdf(x)
    
    def defineCallPut(self):
        d1 = ((math.log(self.So/self.X)) + (self.t*(self.r-self.q+(pow(self.sigma,2)/2))) ) / (self.sigma*math.sqrt(self.t))
        d2 = d1 - (self.sigma*math.sqrt(self.t))
        self.CALL = self.So*math.exp(-self.q*self.t) * self.N(d1)-self.X*math.exp(-self.r*self.t) * self.N(d2)
        self.PUT = self.X*math.exp(-self.r*self.t)*self.N(-d2)-self.So*math.exp(-self.q*self.t)*self.N(-d1)
        self.d1 = d1
        self.d2 = d2
    
    def deltaCall(self):
        return round((math.exp(-self.q*self.t)*self.N(self.d1)),GREEKS_PRECISION)
    
    def deltaPut(self):
        return round((math.exp(-self.q*self.t)*(self.N(self.d1)-1)),GREEKS_PRECISION)
    
    def gamma(self):
        return round(((math.exp(-self.q*self.t))/(self.So*self.sigma*math.sqrt(self.t)))*self.N(self.d1),GREEKS_PRECISION)
    
    def vega(self):
        return round(((1/100)*(self.So*math.exp(-self.q*self.t))*math.sqrt(self.t))*self.N(self.d1),GREEKS_PRECISION)
    
    def rhoCall(self):
        return round(((1/100)*self.X*self.t*math.exp(-self.r*self.t))*self.N(self.d2),GREEKS_PRECISION)
    
    def rhoPut(self):
        return round(((-(1/100))*self.X*self.t*math.exp(-self.r*self.t))*self.N(-self.d2),GREEKS_PRECISION)
    
    def porcentagemAno(self,days,year_size=365):
        return (days*100)/year_size
    
    
           
        