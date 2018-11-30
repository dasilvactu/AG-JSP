#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:26:12 2018

@author: marcus
"""
class JobshopInstance :
    def __init__(self, filename):
        self.ler_instancia(filename)
        #self.nb_activities = self.nb_jobs * self.nb_machines
        self.nb_activities = self.nb_jobs
    # The input files follow the "Taillard" format.
    def ler_instancia(self, filename):
        with open(filename) as f:
            lines = f.readlines()
        first_line = lines[1].split()
        # Number of jobs
        self.nb_jobs = int(first_line[0])
        # Number of machines
        self.nb_machines = int(first_line[1])
        # processing time on each machine for each job (given in the processing order)
        self.processing_time = [[int(lines[i].split()[j]) for j in range(self.nb_machines)] for i in range(3,3+self.nb_jobs)]
        # processing order of machines for each job
        self.job_machine_order = [[int(lines[i].split()[j])-1 for j in range(self.nb_machines)] for i in range(4+self.nb_jobs,4+2*self.nb_jobs)]
        #print(self.job_machine_order)

