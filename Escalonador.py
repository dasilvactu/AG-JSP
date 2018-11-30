#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 14:32:59 2018

@author: marcus
"""
class Scheduler :
    """Scheduler allows to obtain a schedule in output from the priority
        list variables. It is based on the simple J. Giffler and G.L. Thompson
        algorithm (1960)."""
    def __init__(self, instance):
        self.instance = instance
        self.job_progress = [0 for j in range(instance.nb_jobs)]
        self.job_progress_time = [0 for j in range(instance.nb_jobs)]
        self.machine_progress_time = [0 for j in range(instance.nb_machines)]
        self.divisor = max([instance.nb_jobs,instance.nb_machines])
    def schedule(self):
        for i in range(self.instance.nb_machines):
            for k in range(self.instance.nb_activities):
                job = self.priority_list[k] 
                #% self.divisor
                self.schedule_activity(job)
    def schedule_part(self,n):
        for i in range(self.instance.nb_machines):
            for k in range(n):
                job = self.priority_list[k] 
                #% self.divisor
                self.schedule_activity(job)

    def get_make_span(self):
        return max(self.machine_progress_time)

    def call(self, gene):
       # gene = list(unique_everseen(gene))
        
        self.priority_list = gene;
        self.init_lists_attibutes()
        self.schedule()
        #print(self.machine_progress_time)
        return self.get_make_span()
    def call_part(self, gene,n):
       # gene = list(unique_everseen(gene))
        
        self.priority_list = gene;
        self.init_lists_attibutes()
        self.schedule_part(n)
        #print(self.machine_progress_time)
        return self.get_make_span()

    def schedule_activity(self, job):
        m = self.next_machine(job)
        end = self.job_next_activity_end(job)
        #print(job, m, end)
        self.job_progress[job] += 1
        self.machine_progress_time[m] = end
        self.job_progress_time[job] = end

    def job_next_activity_end(self, job):
        next_activity = self.job_progress[job]
        #print(job, next_activity)
        machine = self.instance.job_machine_order[job][next_activity]
        duration = self.instance.processing_time[job][next_activity]
        start = max([self.machine_progress_time[machine], self.job_progress_time[job]])
        return start + duration

    def next_machine(self, job):
        next_activity = self.job_progress[job]
        return self.instance.job_machine_order[job][next_activity]
    def init_lists_attibutes(self):
                self.job_progress = [0 for j in range(self.instance.nb_jobs)]
                self.job_progress_time = [0 for j in range(self.instance.nb_jobs)]
                self.machine_progress_time = [0 for j in range(self.instance.nb_machines)]

