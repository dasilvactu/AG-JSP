#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 14:22:50 2018

@author: marcus
"""

from Instancia import JobshopInstance
import matplotlib.pyplot as plt
from AG import Genetic
from random import seed
instancia = JobshopInstance('instances/Taillard/15_15/15_15_0.txt')
genetico  = Genetic(instancia, 0.2, 0.5, 50, 0.1)
print(genetico.Executa(0,1))
#Mutação 0 - Pairwise interchange neighborhood
#Mutação 1 - Inverse  Mutation
#Mutação 2 - Shift Mutation
#CrossOver 0 - Partially  mapped  crossover
#CrossOver 1 - Linear-Order  crossover
#CrossOver 2 - Order-based Crossover
#CrossOver 3 - Order-Preserving one-point crossover
#vetor = []
#for i in range(5):
#    seed(i+1)
#    vetor.append(genetico.Executa(0,0))
#
##vector = [vector00,vector01,vector02,vector03, vector10, vector11, vector12,vector13,vector20,vector21,vector22,vector23]
#fig, ax = plt.subplots()
##plt.ylim(54,64)
#ax.boxplot(vetor)
#
#plt.show()