import numpy as np 
import networkx as nx
import pandas as pd


# create P table 
def p_table(normal_nodes, Grph, resultpath, name):
    i = 0

    P=np.zeros((len(normal_nodes),len(normal_nodes)))
    m=0
    n=0
    s_sp=1000
    for n_node in normal_nodes:
        for m_node in normal_nodes:
            sp=0
            for node_1 in Grph.nodes:
                x = node_1.split("_")
                j=0
                if (x[0]==n_node):
                    i=i+1;
                    #print (node_1,"->")
                    for node_2 in Grph.nodes:
                        y = node_2.split("_")
                        if (y[0]==m_node):
                            #print (node_2)
                    #try:
                            if nx.has_path(Grph,node_1,node_2):
                                temp=nx.bellman_ford_path_length(Grph,node_1,node_2,'date')
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
    Px.to_csv(resultpath+name+"_P_Matrix.csv")
    print('Matrix P is generated.')
    return Px



def g_table (normal_nodes, G, resultpath, name):
    G_i=np.zeros((len(normal_nodes),len(normal_nodes)))
    i=0
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
                    i=i+1
                    for node_2 in G.nodes:
                        y = node_2.split("_")
                        if (y[0]==m_node):
                            if nx.has_path(G,node_1,node_2):
                                temp=nx.bellman_ford_path_length(G,node_1,node_2)
                                s_sp = min(temp, s_sp)
                                j=1
                    if j==0:
                        i=i-1
                        break
                    sp=sp+s_sp
                    s_sp=1000

            if i!=0:        
                G_i[m][n]=sp/i
                n=n+1
            if i==0:
                G_i[m][n]=np.nan
                n=n+1
            i=0
        n=0
        m=m+1
        
    Gi=pd.DataFrame(G_i,columns=normal_nodes,index=normal_nodes)
    Gx=pd.DataFrame(Gi).copy()
    Gx['Gout']=(Gi.sum(1))/(Gi.count(axis=1)-1)
    Gx.loc['Gin']=Gi.sum()/(Gi.count(axis=0)-1)
    Gx.to_csv(resultpath+name+"_G_Matrix.csv")
    print('Matrix G is generated.')
    return Gx

def v_table(normal_nodes, G, resultpath, name):
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
    Vx.to_csv(resultpath+name+"_V_Matrix.csv")
    print('Matrix V is generated.')
    return Vx