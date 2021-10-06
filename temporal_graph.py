#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 23:53:25 2020

@author: maedehnasri
"""

# Generating temporal graphs


import numpy as np
import pandas as pd
import networkx as nx
from utils import *
from preprocessing import *

# Required files
inputfile = 'Data/test.csv'

# Required path
resultpath = 'Results/'

# Read files
input_file = open(inputfile,"r")
data = pd.read_csv(inputfile,header=0, sep=';')

# additional 
separator = ';'
# Preprocessing
school =0 
preprocess(data, input_file, separator, school)
    

# DataFrame
temp_graph = pd.read_csv('tempdata.txt', sep=",", header=None)
temp_graph.columns = ["sender", "receiver","date"]
senders=temp_graph.sender.unique()
receivers=temp_graph.receiver.unique()
temp_graph=temp_graph.iloc[:,]

# Graph
Grph = nx.from_pandas_edgelist(temp_graph,source='sender', target='receiver', edge_attr='date', create_using=nx.DiGraph())
nodes_list = np.array(list(Grph.nodes()))
normal_nodes=list(set([i.split('_', 1)[0] for i in nodes_list]))
normal_nodes=sorted(normal_nodes, key=str.lower)

# Creating the required data
P = p_table(normal_nodes, Grph, resultpath, name='test')
G = g_table(normal_nodes, Grph, resultpath, name='test')
V = v_table(normal_nodes, Grph, resultpath, name='test')


