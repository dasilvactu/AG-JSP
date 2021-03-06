#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:09:10 2018

@author: marcus
"""
from deap import tools as dp
from Escalonador import Scheduler
from Heuristicas import NEH
import copy
import sys
from random import random, randint, shuffle
class Individual():
    def __init__(self):
        self.gene = []
        self.makespan = 0;
    
    def getGene(self):
        
        return self.gene
    def getMakeSpan(self):
        return self.makespan
    
class Genetic():
    
    def __init__(self, I, txM , txC , popT, LS):
        self.instancia = I
        self.scheduler = Scheduler(self.instancia)
        #self.heuristica = NEH(self.scheduler)
        self.n = self.instancia.nb_activities
        self.txM = txM
        self.txC = txC
        self.popT = popT
        self.stop = (800+10*self.n)*self.n**2
        self.av = 0
        self.LS = LS
    def InitPopulation(self):
        """Generate initial population from random shuffles of the tasks."""
        genotipo = Individual()
        population = []
        genotipo.gene = [j for j in range(self.n)]
        for j in range(int(self.popT- 0.2*self.popT)):
            shuffle(genotipo.gene)
            genotipo.makespan = self.scheduler.call(genotipo.gene)
            self.av+=1
            population.append(genotipo)
        neh = NEH(self.instancia,self.scheduler)
        num_neh = (self.n)*(self.n -1)/2 -2
        genotipo.gene , genotipo.makespan = neh.neh()
        self.av+=num_neh 
        genotipo.makespan = self.scheduler.call(genotipo.gene)
        for i in range(int(0.2*self.popT)):
            population.append(genotipo)
        return population
    def LocalSearch(self, gene):
        seq_current = copy.deepcopy(gene)
        n_jobs = int(len(gene)*self.LS)
        lista = []
        for i in range(n_jobs):
            index = randint(0,len(seq_current)-1)
            lista.append(seq_current.pop(index))
        for i in range(len(lista)):
            min_cmax = float("inf")
            value = lista[i]
            for j in range(0, len(seq_current) + 1):
                tmp_seq = self.insertion(seq_current, j, value)
                cmax_tmp = self.scheduler.call_part(tmp_seq,len(tmp_seq))
                self.av+=1
                #print(tmp_seq, cmax_tmp)
                if min_cmax > cmax_tmp:
                    best_seq = tmp_seq
                    min_cmax = cmax_tmp
            seq_current = best_seq
        return seq_current, self.scheduler.call(seq_current)
    def insertion(self,sequence, index_position, value):
        new_seq = sequence[:]
        new_seq.insert(index_position, value)
        return new_seq    
    def Avalia(self, gene ):
        return self.scheduler.call(gene)
    
    def CrossoverLOX(self, p1,p2):
        nt = self.n
        filho1 = Individual()
        filho2 = Individual()
        i = randint(0,nt-1)
        j = randint(0,nt-1)
        i,j = min(i,j),max(i,j)
        mid1 = p1.gene[i:j]
        mid2 = p2.gene[i:j]
        resto1 = [j for j in p2.gene if j not in mid1]
        resto2 = [j for j in p1.gene if j not in mid2]
        left1 = resto1[:i]
        left2 = resto2[:i]
        right1 = resto1[i:]
        right2 = resto2[i:]
        filho1.gene= [j for j in left1 + mid1+ right1]
        filho2.gene= [j for j in left2 + mid2+ right2]
        #filho1.gene, filho2.gene = dp.cxTwoPoint(p1.gene, p2.gene)
        return filho1,filho2
    
    def CrossoverOPX(self, p1, p2):
        nt = self.n
        filho1 = Individual()
        filho2 = Individual()
        i = randint(0,nt-1)
        left1 = p1.gene[:i]
        right1 = [j for j in p2.gene if j not in left1]
        left2 = p2.gene[:i]
        right2 = [j for j in p1.gene if j not in left2]
        filho1.gene= [j for j in left1 + right1]
        filho2.gene= [j for j in left2 + right2]
        #filho1.gene, filho2.gene = dp.cxOnePoint(p1.gene, p2.gene)
        return filho1,filho2
    
    def CrossoverPMX(self, p1, p2):
        filho1 = Individual()
        filho2 = Individual()
        filho1.gene, filho2.gene = dp.cxPartialyMatched(p1.gene, p2.gene)
        return filho1,filho2
    
    def CrossoverOBX(self, p1, p2):
        filho1 = Individual()
        filho2 = Individual()
        filho1.gene, filho2.gene = dp.cxOrdered(p1.gene, p2.gene)
        return filho1,filho2
    
    def MutationIM(self, p):
        nt = self.n
        i = randint(0, nt - 1)
        j = randint(0, nt - 1)
        filho = Individual()
        filho.gene = p.gene
        filho.gene[i], filho.gene[j] = filho.gene[j], filho.gene[i]
        return filho
    
    def MutationSM(self, p):
        posicao = randint(0, self.n -1)
        corte = randint(0, self.n -1)
        left = p.gene[:corte]
        right = p.gene[corte:]
        if(posicao < corte):
            left.remove(p.gene[posicao])
        else:
            right.remove(p.gene[posicao])
        left.append(p.gene[posicao])
        toda = [j for j in left + right]
        filho = Individual()
        filho.gene = toda
        return filho
    
    def MutationIN(self ,p):
        corte1 = randint(0, self.n -1)
        corte2 = randint(0, self.n -1)
        menor = min(corte1,corte2)
        maior = max(corte1,corte2)
        left = p.gene[:menor]
        meio = []
        meio = p.gene[menor:maior]
        right = p.gene[maior:]
        meio.reverse();
        toda = [j for j in left + meio+right]
        filho = Individual()
        filho.gene = toda
        return filho
    
    def Torneio(self, pop, tam):
        i = randint(0, tam -1)
        j = randint(0, tam -1)
        return max(i,j)
    def Mutation(self,mut, ind):
        if mut ==0:
            return self.MutationIM(ind)
        elif mut==1:
            return self.MutationIN(ind)
        elif mut==2:
            return self.MutationSM(ind)
            
    def CrossOver(self, cross, ind1, ind2):
        if cross ==0:
            return self.CrossoverPMX(ind1,ind2)
        elif cross==1:
            return self.CrossoverLOX(ind1,ind2)
        elif cross==2:
            return self.CrossoverOBX(ind1,ind2)
        elif cross==3:
            return self.CrossoverOPX(ind1,ind2)
        
    def Executa(self,mut, cross):
        best = sys.maxsize
        pop = [g for g in self.InitPopulation()]
        pop.sort(key= Individual.getMakeSpan)
        while self.av < self.stop:
            #print(it)
            flag = 0
            i = self.Torneio(pop, self.popT)
            j = self.Torneio(pop, self.popT)
            ind1 = copy.deepcopy(pop[i])
            ind2 = copy.deepcopy(pop[j])
            if(self.txC<=random()):
                ind1, ind2= self.CrossOver(cross,pop[i],pop[j])
                ind1.makespan = self.scheduler.call(ind1.gene)
                ind2.makespan = self.scheduler.call(ind2.gene)
                self.av+=2
                flag = 3
            if(self.txM<=random()):
                ind1 = self.Mutation(mut,ind1)
                ind1.makespan = self.scheduler.call(ind1.gene)
                self.av+=1
                flag = 1
            if(self.txM<=random()):
                ind2 = self.Mutation(mut,ind2)
                ind2.makespan = self.scheduler.call(ind2.gene)
                self.av+=1
                flag = 2
            if flag ==1:
                ind1.gene, ind1.makespan = self.LocalSearch(ind1.gene)
            elif cross==2:
                ind2.gene, ind2.makespan = self.LocalSearch(ind2.gene)
            elif cross==3:
                ind1.gene, ind1.makespan = self.LocalSearch(ind1.gene)
                ind2.gene, ind2.makespan = self.LocalSearch(ind2.gene)
            pop.append(ind1)
            pop.append(ind2)
            pop.sort(key= Individual.getMakeSpan)
            pop = pop[:self.popT]
            if(pop[0].makespan< best):
                best = pop[0].makespan
                #print(" - Makespan: ", best)
            #print(self.av)
        #print(pop[0].gene, " - Makespan:", pop[0].makespan)
        return best
