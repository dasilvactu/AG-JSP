#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 20:16:55 2018

@author: marcus
"""
class NEH():
    def __init__(self,instancia,scheduler):
        self.sch = scheduler
        self.instancia = instancia
        self.machines = instancia.nb_machines
        self.jobs = instancia.nb_jobs
    def sum_processing_time(self):
        sum_pt = [[sum(self.instancia.processing_time[i]),i] for i in range(self.jobs)]
        ordenado = sorted(sum_pt, key=lambda x: x[0], reverse=True)
        return [ordenado[i][1] for i in range(self.jobs)]
    def insertion(self,sequence, index_position, value):
        new_seq = sequence[:]
        new_seq.insert(index_position, value)
        return new_seq
    def neh(self):
        order_seq = self.sum_processing_time()
        #order_seq = [i for i in order_seq[1]]
        #print(order_seq)
        seq_current = [order_seq[0],order_seq[1]]
        for i in range(2, self.instancia.nb_jobs):
            min_cmax = float("inf")
            value = order_seq[i]
            #print(i,"-",value)
            for j in range(0, i + 1):
                tmp_seq = self.insertion(seq_current, j, value)
                cmax_tmp = self.sch.call_part(tmp_seq,len(tmp_seq))
                #print(tmp_seq, cmax_tmp)
                if min_cmax > cmax_tmp:
                    best_seq = tmp_seq
                    min_cmax = cmax_tmp
            seq_current = best_seq
        return seq_current, self.sch.call(seq_current)
    
        