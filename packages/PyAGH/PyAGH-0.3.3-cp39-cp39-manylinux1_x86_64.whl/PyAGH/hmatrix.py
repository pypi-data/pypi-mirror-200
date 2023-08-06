import pandas as pd
import numpy as np
from numbers import Number
import sympy

def makeH(G,A,w=0.05):
    '''Calculate the additive kinship matrix using genotype and pedigree.

    G: a list with two elements, G[0] is kinship matrix based on genotype; G[1] is id series of genotyped individuals.
    A: a list with two elements, A[0] is kinship matrix based on pedigree; A[1] is id series of all individuals.
    w: Default value is 0.05. The weights of the G-matrix and the A-matrix
    '''

    ##Check whether the provided parameters are correct. The list includes two elements, the first is an np matrix, and the second is a series. The length of both must be consistent. W is a number
    ##A[0],G[0] Nan
    if not isinstance(G, list):
        print("ERROR: Parameter G should be a list!")
        return
    if len(G) != 2:
        print("ERROR: G should have 2 elements")
        return
    if not isinstance(G[1], pd.Series):
        print("ERROR: G should have 2 elements with numpy ndarray and pandas Series")
        return
    if not isinstance(G[0], np.ndarray):
        print("ERROR: G should have 2 elements with numpy ndarray and pandas Series")
        return
    if np.isnan(G[0]).any():
        print("ERROR: Nan in G")
        return
    if G[0].shape[0] != len(G[1]):
        print("ERROR: The dimension of G is not equal to the number of individual with genotyped")
        return
    ####A
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
        ## W
    if not isinstance(w, Number):
        print("ERROR: Parameter w should be a number")
        return
    
    if w<0 or w>1:
        print("ERROR: Parameter w should between 0 and 1")
        return
    
    ##We need to check if all the sequenced individuals are in the pedigree
    A[1] = A[1].astype(str)
    G[1] = G[1].astype(str)
    if not all(G[1].isin(A[1])):
        print("ERROR: not all individuals with genotyped are in A matrix")
        return

    geno_id_loc = A[1][A[1].isin(G[1])] 
    index_geno = geno_id_loc.iloc[list(map(geno_id_loc.tolist().index,G[1]))].index ###The index extracted in the A-matrix in the order of the sequencing individuals provided
    index_nogeno = A[1][~A[1].isin(G[1])].index ##Index of the remaining non sequenced individuals
    ##subset
    A11 = A[0][index_nogeno,:][:,index_nogeno]
    A12 = A[0][index_nogeno,:][:,index_geno]
    A21 = A[0][index_geno,:][:,index_nogeno]
    A22 = A[0][index_geno,:][:,index_geno]
    iA22 = np.linalg.inv(A22)
    ave_dia_G = np.trace(G[0])/G[0].shape[0]
    ave_offdia_G = (np.sum(G[0])-np.trace(G[0]))/(G[0].shape[0]*G[0].shape[0]-G[0].shape[0])
    ave_dia_A22 = np.trace(A22)/A22.shape[0]
    ave_offdia_A22 = (np.sum(A22)-np.trace(A22))/(A22.shape[0]*A22.shape[0]-A22.shape[0])
    a = sympy.Symbol("a")
    b = sympy.Symbol("b")
    ab = sympy.solve([ave_dia_G*b+a-ave_dia_A22,ave_offdia_G*b+a-ave_offdia_A22],[a,b])

    G_star = ab[a]+ab[b]*G[0]

    G_w = (1-w) * G_star + w * A22
    G_w =np.around(G_w.astype(float),6)

    H11 = A11+A12.dot(iA22).dot(G_w-A22).dot(iA22).dot(A21)
    H12 = A12.dot(iA22).dot(G_w)
    H21 = G_w.dot(iA22).dot(A21)
    H22 = G_w
    H = np.round(np.hstack((np.vstack((H11,H21)),np.vstack((H12,H22)))),2)
    return [H,pd.concat([A[1][index_nogeno], A[1][index_geno]]).reset_index(drop=True)]
    