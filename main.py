#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 23:53:25 2020

@author: maedehnasri
"""

# Generating temporal graphs - Schoolyard


import numpy as np
import pandas as pd
import networkx as nx
from utils import *
from preprocessing import *
import argparse


# parser = argparse.ArgumentParser()
# parser.add_argument('--basicinfo', type=str, default='Basic_info.csv',
#                     help='Path and file name of the basic information')
# parser.add_argument('--edgefile', type=str, default='edge_code_098.csv',
#                     help='Path and file name of the edge file')
# parser.add_argument('--numdata', type=int, default=20000,
#                     help='Number of data to read')
# parser.add_argument('--resultpath', type=str, default='',
#                     help='Path to the result files')


# args = parser.parse_args()

# Required files
root ='/Users/maedehnasri/Documents/Data/Results/12/01/' 
inputfile = root + '12_12111088_20201112_01_TH_35_00_mirrored_edge_list.csv'
info_file = '/Users/maedehnasri/Documents/Data/Protocols/2_basic_info.csv'

# Required path
resultpath = 'Results/' 

# additional 
seperator = ','
# Read files
data = pd.read_csv(inputfile,header=0, sep=seperator, index_col=0)

basicinfo = pd.read_csv(info_file,sep=';')
basicinfo['Code']=basicinfo['Code'].astype(np.int64)
basicinfo = basicinfo.fillna(0)

# Refine edges 
database, file_name = find_interactions(data)

input_file = open(file_name,"r")
# Preprocessing
schools=1
preprocess(database, input_file, seperator, schools)
    

# DataFrame
temp_graph = pd.read_csv('tempdata.txt', sep=",", header=None)
temp_graph.columns = ["sender", "receiver","date"]
senders=temp_graph.sender.unique()
receivers=temp_graph.receiver.unique()
temp_graph=temp_graph.iloc[:10,]

# Graph
Grph = nx.from_pandas_edgelist(temp_graph,source='sender', target='receiver', edge_attr='date', create_using=nx.DiGraph())
nodes_list = np.array(list(Grph.nodes()))
normal_nodes=list(set([i.split('_', 1)[0] for i in nodes_list]))
normal_nodes=sorted(normal_nodes, key=str.lower)

# Creating the required data
P = p_table(normal_nodes, Grph, resultpath, name='12')
G = g_table(normal_nodes, Grph, resultpath, name='12')
V = v_table(normal_nodes, Grph, resultpath, name='12')


