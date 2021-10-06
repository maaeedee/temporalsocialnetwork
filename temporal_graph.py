#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 23:53:25 2020

@author: maedehnasri
"""

#### Generating temporal graphs_ De Kristal School
#### Generating temporal graphs_ De Kristal School


import networkx as nx
import pandas as pd
import numpy as np


def attach_instance (device, date):
    #global last_seen
    # see if a device has appeared previously. If so, create a directed link
    # from previous instance to this instance.
    # time difference between the two instances
    previous_date=last_seen[device]
    if (previous_date != "")and (previous_date!= date):
        diff = abs(date - previous_date);
        #print (device,",",previous_date,",",device,",",date,",",diff,"\n")
        f.write("%s_%d,%s_%d,%d \r\n"%(device,previous_date,device,date,diff))
    last_seen[device]=date;

#f.write("Appended line %d\r\n" % (i+1))
inputfile = 'Data/test.csv'
resultpath = 'Results/'
input_file = open(inputfile,"r")
data = pd.read_csv(inputfile,header=0, sep=';')
f= open("tempdata.txt","w+")

column_values = data[["Sender", "Receiver"]].values.ravel()
unique_values =  pd.unique(column_values)
#last_seen=dict.fromkeys(['"A"','"B"','"C"','"D"','"E"'],"")
last_seen=dict.fromkeys((unique_values),'')
#previous_date=0
try:
    next(input_file)
    for i, line in enumerate (input_file):
        line=line.replace('"', '').strip()
        items=line.split(';')
        date=int(items[2])
        sender = str(items[0])
        recepient = str(items[1].replace("\n",""))
        attach_instance(sender,date)
        attach_instance(recepient,date)
        #print (sender,",",date,",",recepient,",",date,",","0\n")
        #print (recepient,",",date,",",sender,",",date,",","0\n")
        f.write("%s_%d,%s_%d,0 \r\n"%(sender,date,recepient,date))
        f.write("%s_%d,%s_%d,0 \r\n"%(recepient,date,sender,date))
        
        
finally:
    input_file.close()
    f.close()
    

#allnodes_nd = [next(iter(filter(None, values)), '') for values in zip(calleee, callerr)]


temp_graph = pd.read_csv('tempdata.txt', sep=",", header=None)
temp_graph.columns = ["sender", "receiver","date"]

senders=temp_graph.sender.unique()
receivers=temp_graph.receiver.unique()

temp_graph=temp_graph.iloc[:,]
#temp_graph

G = nx.from_pandas_edgelist(temp_graph,source='sender', target='receiver', edge_attr='date', create_using=nx.DiGraph())

#nx.draw(G)

nodes_list = np.array(list(G.nodes()))

normal_nodes=list(set([i.split('_', 1)[0] for i in nodes_list]))
normal_nodes=sorted(normal_nodes, key=str.lower)
#normal_nodes


P=np.zeros((len(normal_nodes),len(normal_nodes)))
m=0
n=0
s_sp=1000
for n_node in normal_nodes:
    for m_node in normal_nodes:
        sp=0
        for node_1 in G.nodes:
            x = node_1.split("_")
            j=0
            if (x[0]==n_node):
                i=i+1;
                #print (node_1,"->")
                for node_2 in G.nodes:
                    y = node_2.split("_")
                    if (y[0]==m_node):
                        #print (node_2)
                #try:
                        if nx.has_path(G,node_1,node_2):
                            temp=nx.bellman_ford_path_length(G,node_1,node_2,'date')
                            s_sp = min(temp, s_sp)
                            j=1
                            #print(s_sp)
                if j==0:
                    i=i-1
                    #print("*")
                    break
                sp=sp+s_sp
                #print("1; sp=",sp)
                s_sp=1000000

        if i!=0:        
            P[m][n]=sp/i
            n=n+1
        if i==0:
            P[m][n]=np.nan
            n=n+1
        #sp=0
        #print("m=",m)
        i=0
    n=0
    m=m+1

Pi=pd.DataFrame(P,columns=normal_nodes,index=normal_nodes)

Px=pd.DataFrame(Pi)
Px['Pout']=(Pi.sum(1))/(Pi.count(axis=1)-1)
Px.loc['Pin']=Pi.sum()/(Pi.count(axis=0)-1)
Px.to_csv(resultpath+"test_P_Matrix.csv")

#Pi.count(axis=0)

G_i=np.zeros((len(normal_nodes),len(normal_nodes)))
m=0
n=0
s_sp=1000
for n_node in normal_nodes:
    for m_node in normal_nodes:
        sp=0
        for node_1 in G.nodes:
            x = node_1.split("_")
            j=0
            if (x[0]==n_node):
                i=i+1;
                #print (node_1,"->")
                for node_2 in G.nodes:
                    y = node_2.split("_")
                    if (y[0]==m_node):
                        #print (node_2)
                #try:
                        if nx.has_path(G,node_1,node_2):
                            temp=nx.bellman_ford_path_length(G,node_1,node_2)
                            s_sp = min(temp, s_sp)
                            j=1
                            #print(s_sp)
                if j==0:
                    i=i-1
                    #print("*")
                    break
                sp=sp+s_sp
                #print("1; sp=",sp)
                s_sp=1000

        if i!=0:        
            G_i[m][n]=sp/i
            n=n+1
        if i==0:
            G_i[m][n]=np.nan
            n=n+1
        #sp=0
        #print("m=",m)
        i=0
    n=0
    m=m+1
    


Gi=pd.DataFrame(G_i,columns=normal_nodes,index=normal_nodes)
Gx=pd.DataFrame(Gi)
Gx['Gout']=(Gi.sum(1))/(Gi.count(axis=1)-1)
Gx.loc['Gin']=Gi.sum()/(Gi.count(axis=0)-1)
Gx.to_csv(resultpath+"test_G_Matrix.csv")

V_i=np.zeros((len(normal_nodes),len(normal_nodes)))
m=0
n=0
c=0
i=0
s_sp=1000
for n_node in normal_nodes:
    for m_node in normal_nodes:
        sp=0
        for node_1 in G.nodes:
            x = node_1.split("_")
            j=0
            if (x[0]==n_node):
                i=i+1
                c=c+1
                #print (node_1,"->")
                for node_2 in G.nodes:
                    y = node_2.split("_")
                    if (y[0]==m_node):
                        if nx.has_path(G,node_1,node_2): 
                            j=1

                if j==0:
                    i=i-1

        V_i[m][n]=i/c
        n=n+1
        i=0
        c=0
    n=0
    m=m+1
    

Vi=pd.DataFrame(V_i,columns=normal_nodes,index=normal_nodes)

Vx=pd.DataFrame(Vi)
Vx['Vout']=(Vx.sum(1)-1)/(len(normal_nodes)-1)
Vx.loc['Vin']=(Vx.sum()-1)/(Vx.count(axis=0)-1)

Vx.to_csv(resultpath+"test_V_Matrix.csv")


