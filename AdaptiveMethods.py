# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 18:50:19 2018

@author: Marcus Vinicius
"""
import numpy as np
class AdaptivePersuit:
    def __init__(self,K,Pmin,alpha, beta):
        self.Q = []
        self.P = []
        self.K = K
        self.Pmin = Pmin
        self.alpha = alpha
        self.beta = beta
        self.Pmax = 1 - (K -1)*self.Pmin
        for i in range(K):
            self.P.append(1/self.K)
            self.Q.append(1.0)
    def atualiza(self, R , i):
        self.Q[i] = self.Q[i] + self.alpha*(R[i] - self.Q[i])
        i_best = np.argmax(self.Q)
        self.P[i_best]= self.P[i_best] + self.beta*(self.Pmax - self.P[i_best])
        for j in range(self.K):
            if j!=i_best:
                self.P[j]= self.P[j] + self.beta*(self.Pmin - self.P[j])
        
#class RankedMultiArmedBandit:
    
#class SlidingMultiArmedBandit: