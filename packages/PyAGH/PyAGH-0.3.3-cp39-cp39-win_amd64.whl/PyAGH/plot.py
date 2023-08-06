from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as pt
import pandas as pd
import numpy as np
from .sort import sortPed
def cluster(A,color_threshold=0.9,above_threshold_color='gray'):
    '''Plot the cluster of kinship matrix.

    A: a list with two elements, A[0] is kinship matrix; A[1] is id series of all individuals.
    '''
    if not isinstance(A, list):
        print("ERROR: Parameter A should be a list!")
        return
    if len(A) != 2:
        print("ERROR: A should have 2 elements")
        return
    if not isinstance(A[1], pd.Series):
        print("ERROR: A should have 2 elements with numpy ndarray and pandas Series")
        return
    if not isinstance(A[0], np.ndarray):
        print("ERROR: A should have 2 elements with numpy ndarray and pandas Series")
        return
    if np.isnan(A[0]).any():
        print("ERROR: Nan in A")
        return
    if A[0].shape[0] != len(A[1]):
        print("ERROR: The dimension of A is not equal to the number of individual with genotyped")
        return
    Z = hierarchy.linkage(A[0], method ='average',metric='euclidean')
    P = hierarchy.dendrogram(Z,labels=list(A[1]),color_threshold=color_threshold, 
                      above_threshold_color=above_threshold_color)
    return P

def pca(A,group,color=[]):
    '''Plot the PCA of kinship matrix.

    A: a list with two elements, A[0] is kinship matrix; A[1] is id series of all individuals.
    group: a list containing information about the group of individuals.
    '''
    if not isinstance(A, list):
        print("ERROR: Parameter A should be a list!")
        return
    if len(A) != 2:
        print("ERROR: A should have 2 elements")
        return
    if not isinstance(A[1], pd.Series):
        print("ERROR: A should have 2 elements with numpy ndarray and pandas Series")
        return
    if not isinstance(A[0], np.ndarray):
        print("ERROR: A should have 2 elements with numpy ndarray and pandas Series")
        return
    if np.isnan(A[0]).any():
        print("ERROR: Nan in A")
        return
    if A[0].shape[0] != len(A[1]):
        print("ERROR: The dimension of A is not equal to the number of individual with genotyped")
        return
    if len(group) != len(A[1]):
        print("ERROR: The dimension of A is not equal to the length of group.")
        return
    [eigValue, V] = np.linalg.eig(A[0])
    index = np.argsort(-eigValue)
    V = V[:,index]
    eigValue = eigValue[index]
    explained_variance = eigValue / (A[0].shape[0])   # Get variance explained by singular values
    total_var = explained_variance.sum()
    explained_variance_ratio = explained_variance / total_var 
    var=np.cumsum(np.round(explained_variance_ratio, decimals=3)*100)

    plt.figure(figsize=(16,7))
    myfig = plt.gcf()
    ax = plt.subplot(121)
    ax.plot(list(range(1,len(var)+1)), var)
    ax.set_title("PCA Variance Explained Based on Custom PCA")
    ax.set_ylabel("% Variance Explained")
    ax.set_xlabel("# Of Features")

    pcs = pd.DataFrame({"group":group,
    "PC1":V[:,0],
    "PC2":V[:,1]
            })
    levels, categories = pd.factorize(pcs['group'])
    if len(color)==0: 
        colors = [plt.cm.tab10(i) for i in levels]  
    else:
        colors = color
    ax = plt.subplot(122)
    ax.scatter(pcs['PC1'], pcs['PC2'], c=colors)
    x_label = 'PC1(%s%%)' % round((explained_variance_ratio[0]*100.0),2)  
    y_label = 'PC2(%s%%)' % round((explained_variance_ratio[1]*100.0),2)   
    ax.set_xlabel(x_label)    
    ax.set_ylabel(y_label)    
    ax.set_title("PCA plot of top 2 PCs")

    handles = [pt.Patch(color=plt.cm.tab10(i), label=c) for i, c in enumerate(categories)]
    ax.legend(handles=handles,  title='Group')
    return myfig

def heat(A):
    '''Plot the heatmap of kinship matrix.

    A: a list with two elements, A[0] is kinship matrix; A[1] is id series of all individuals.
    '''
    if not isinstance(A, list):
        print("ERROR: Parameter A should be a list!")
        return
    if len(A) != 2:
        print("ERROR: A should have 2 elements")
        return
    if not isinstance(A[1], pd.Series):
        print("ERROR: A should have 2 elements with numpy ndarray and pandas Series")
        return
    if not isinstance(A[0], np.ndarray):
        print("ERROR: A should have 2 elements with numpy ndarray and pandas Series")
        return
    if np.isnan(A[0]).any():
        print("ERROR: Nan in A")
        return
    if A[0].shape[0] != len(A[1]):
        print("ERROR: The dimension of A is not equal to the number of individual with genotyped")
        return
    fig = plt.figure()
 
    myfig = plt.gcf()
    ax = fig.add_subplot(111)
   
    ax.set_yticks(range(len(A[1])))
    ax.set_yticklabels(A[1])
    ax.set_xticks(range(len(A[1])))
    ax.set_xticklabels(A[1])
   
    im = ax.imshow(A[0], cmap=plt.cm.summer)
  
    plt.colorbar(im)
  
    plt.title("Heatmap of relationship matrix")

    return myfig
def gragh(data_ord,color_sire="blue",color_dam="red",fillcolor_sire="lightblue",fillcolor_dam="pink"):
    '''Plot family tree in three generations of a individual.

    data_ord: the pedigree of one individual in three generations.
    '''
    data_ord = sortPed(data_ord)

    if data_ord.shape[0]>15:
        print("Error: Please provide an individual's three-generation pedigree, which should not exceed 15 records at most")
        print("You can selectPed function first to select ped")
        return

    plotid = data_ord[~data_ord.iloc[:,0].isin(pd.concat([data_ord.iloc[:,1],(data_ord.iloc[:,2])]).to_list())]
    if plotid.shape[0] != 1:
        print("Error: Please provide one individual's three-generation pedigree, which should not exceed 15 records at most")
        print("You can selectPed function first to select ped")
        return
    id_15 = plotid.iloc[0,0]
    id_7 = plotid.iloc[0,1]
    id_14 = plotid.iloc[0,2]
    if id_7 == '0':
        id_3 = id_6 = id_1 =id_2 =id_4 = id_5 ='0'
    else:
        id_3 = data_ord[data_ord.iloc[:,0] == id_7].iloc[0,1]
        id_6 = data_ord[data_ord.iloc[:,0] == id_7].iloc[0,2]
        if id_3 == '0':
            id_1 =id_2 ='0'
        else:
            id_1 =data_ord[data_ord.iloc[:,0] == id_3].iloc[0,1]
            id_2 =data_ord[data_ord.iloc[:,0] == id_3].iloc[0,2]
        if id_6 =='0':
            id_4 = id_5 ='0'
        else:
            id_4 =data_ord[data_ord.iloc[:,0] == id_6].iloc[0,1]
            id_5 =data_ord[data_ord.iloc[:,0] == id_6].iloc[0,2]
    if id_14 == '0':
        id_8 = id_9 = id_10 =id_11 =id_12 = id_13 ='0'
    else:
        id_10 = data_ord[data_ord.iloc[:,0] == id_14].iloc[0,1]
        id_13 = data_ord[data_ord.iloc[:,0] == id_14].iloc[0,2]
        if id_10 =='0':
            id_8 = id_9 ='0'
        else:
            id_8 = data_ord[data_ord.iloc[:,0] == id_10].iloc[0,1]
            id_9 = data_ord[data_ord.iloc[:,0] == id_10].iloc[0,2]
        if id_13 =='0':
            id_11 = id_12 ='0'
        else:
            id_11 = data_ord[data_ord.iloc[:,0] == id_13].iloc[0,1]
            id_12 = data_ord[data_ord.iloc[:,0] == id_13].iloc[0,2]
    a ='''digraph G {{
  edge [dir=none];
  node [shape=box];
  graph [splines=ortho];
 
  1     [shape=box, label="{0}",regular=0, color="{15}", style="filled" fillcolor="{17}"] ;
  2     [shape=oval,label="{1}", regular=0, color="{16}", style="filled" fillcolor="{18}"] ;
  3     [group =g1,label="{2}",shape=box, regular=0, color="{15}", style="filled" fillcolor="{17}"] ;
  4    [shape=box, label="{3}",regular=0, color="{15}", style="filled" fillcolor="{17}"] ;
  5   [shape=oval, label="{4}",regular=0, color="{16}", style="filled" fillcolor="{18}"] ;
  6   [group =g2,label="{5}",shape=oval, regular=0, color="{16}", style="filled" fillcolor="{18}"] ;
  7      [group =g3,label="{6}",shape=box, regular=0, color="{15}", style="filled" fillcolor="{17}"] ;
  8     [shape=box, label="{7}",regular=0, color="{15}", style="filled" fillcolor="{17}"] ;
  9     [shape=oval, label="{8}",regular=0, color="{16}", style="filled" fillcolor="{18}"] ;
  10      [group =b1,label="{9}",shape=box, regular=0, color="{15}", style="filled" fillcolor="{17}"] ;
  11     [shape=box,label="{10}", regular=0, color="{15}", style="filled" fillcolor="{17}"] ;
  12    [shape=oval,label="{11}", regular=0, color="{16}", style="filled" fillcolor="{18}"] ;
  13     [group =b2,label="{12}",shape=oval, regular=0, color="{16}", style="filled" fillcolor="{18}"] ;
  14    [group =b3,label="{13}",shape=oval, regular=0, color="{16}", style="filled" fillcolor="{18}"] ;
  15   [group =c1,label="{14}",shape=box, regular=0, color="{15}", style="filled" fillcolor="{17}"] ;


  '''.format(id_1,id_2,id_3,id_4,id_5,id_6,id_7,id_8,id_9,id_10,id_11,id_12,id_13,id_14,id_15,color_sire,color_dam,fillcolor_sire,fillcolor_dam)+'''
  a1 [shape=diamond,label="",height=0.25,width=0.25,group =g1];
  {rank=same; 1 -> a1 -> 2};
  a1 -> 3
  a2 [shape=diamond,label="",height=0.25,width=0.25,group =g2];
  {rank=same; 4 -> a2 -> 5};
  a2-> 6
  t1 [style=invis,shape=point,width=0.0,group =g3];
  {edge[ style=invis];rank = same; 2->t1->4;}

  a3 [shape=diamond,label="",height=0.25,width=0.25,group =g3];
  {rank=same; 3 -> a3 -> 6};
  
  a3-> 7
  {edge[style=invis]; t1->a3;}

  b1 [shape=diamond,label="",height=0.25,width=0.25,group =b1];
  {rank=same; 8 -> b1 -> 9};
  b1 -> 10
  b2 [shape=diamond,label="",height=0.25,width=0.25,group =b2];
  {rank=same; 11 -> b2 -> 12};
  b2 -> 13

  t2 [style=invis,shape = point,width=0.1,group =b3];
  {edge[ style=invis];rank = same; 9->t2->11;}

  b3 [shape=diamond,label="",height=0.25,width=0.25,group =b3];
  {rank=same; 10 -> b3 -> 13};
  
  b3 -> 14
  {edge[style=invis]; t2->b3;}
  c1 [shape=diamond,label="",height=0.25,width=0.25,group =c1];
  {rank=same; 7 -> c1 -> 14};
  c1 -> 15

  
  {
  rank = same;
  edge[ style=invis];
  3 -> 6 -> 10 -> 13 ;
  rankdir = LR;
  }

}'''
    return a