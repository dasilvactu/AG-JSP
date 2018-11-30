# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:14:41 2018

@author: Marcus Vinicius
"""

from Instancia import JobshopInstance
from AGA_AP_RI import GeneticAdaptive
instancia = JobshopInstance('instances/Taillard/15_15/15_15_0.txt')
genetico  = GeneticAdaptive(instancia, 50, 7, 0.05, 0.2, 0.2, 0.1)
print(genetico.Executa())