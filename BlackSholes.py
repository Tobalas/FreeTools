# -*- coding: utf-8 -*-
'''
Created on 11 de jun de 2019

@author: johanes
'''
import math

from scipy.stats import norm

DECIMAL_GREGOS = 2     
class Formula():
    def __init__(self,So,X,sigma,r,q,t):
        self.So = So # preco do ativo
        self.X = X # preco de strike
        self.sigma = sigma/100 # volatilidade
        self.r = r/100 #taxa selic
        self.q = q/100 #dividend yeld
        self.t = self.porcentagemAno(t) /100  # tempo até o vencimento em dias
        
        self.CALL = False
        self.PUT = False
        
        self.d1 = 0
        self.d2 = 0
    
    
    
    def Nx(self,x):
        ''' standard normal probability density function'''
        
        e = math.exp(-x**2/2)/math.sqrt(2*math.pi)
        return e
    
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
        return round((math.exp(-self.q*self.t)*self.N(self.d1)),DECIMAL_GREGOS)
    
    def deltaPut(self):
        return round((math.exp(-self.q*self.t)*(self.N(self.d1)-1)),DECIMAL_GREGOS)
    
    def gamma(self):
        return round(((math.exp(-self.q*self.t))/(self.So*self.sigma*math.sqrt(self.t)))*self.N(self.d1),DECIMAL_GREGOS)
    
    def thetaCall(self):
        return 'WHAT?'
    
    def thetaPut(self):
        return 'WUT?'
    
    def vega(self):
        return round(((1/100)*(self.So*math.exp(-self.q*self.t))*math.sqrt(self.t))*self.N(self.d1),DECIMAL_GREGOS)
    
    def rhoCall(self):
        return round(((1/100)*self.X*self.t*math.exp(-self.r*self.t))*self.N(self.d2),DECIMAL_GREGOS)
    
    def rhoPut(self):
        return round(((-(1/100))*self.X*self.t*math.exp(-self.r*self.t))*self.N(-self.d2),DECIMAL_GREGOS)
    
    def porcentagemAno(self,dias):
        return (dias*100)/365
    
    
           
        