#!/usr/bin/env python

import itertools
import rpy2.robjects as ro
import sys

try:
    ro.r(r"library('Vennerable')")
except RRuntimeError:
    print "Unable to load Vennerable in R, make sure it's properly installed" 
    sys.exit(1)
    
    
def makeSubsets(S):
    '''
    Arguments:
        S -  List of sets to make in to a Venn diagram
    Takes a list of sets a list of the sizes of non-overlapping intersections between them 
    '''
    
    if any([type(s) != set for s in S]):
        raise TypeError("Arguments must be a list of sets")

    N = len(S)
    
    # Generate a truth table of intersections to calculate 
    truth_table = [x for x in itertools.product("01", repeat=N)][1:]

    
    weights = {}
    for t in truth_table:
        ones = [S[i] for i in range(N) if t[i] =='1']
        zeros = [S[i] for i in range(N) if t[i] =='0']
        
        X = set.intersection(*ones)
        X.difference_update(*zeros)
        
        weights[''.join(t)] = len(X)
    
    return(weights)
        

def Venn(S, labels, r_name = 'x', venn_kwargs = {}, plot_kwargs = {}):
    '''
    Arguments:
        S -  List of sets to make in to a Venn diagram
        labels - List of names of the sets
        r_name - R object name to save Venn diagram to 
        venn_kwargs - Dict of args passed directly to Vennerable.Venn()
        plot_kwargs - Dict of args passed directly to plot()
        
    '''
    
    assert len(S) == len(labels), "Number of labels must match number of sets"
    
    weights = makeSubsets(S) 
    weight_string = "c(" + ", ".join(["\'" + k + "\'=" + str(v) for k,v in weights.items() ]) + ")"
    
    ven_kw = ", ".join([k + " = " + v for k,v in venn_kwargs.items()])    
    plot_kw = ", ".join([k + " = " + v for k,v in plot_kwargs.items()])    
    
    lab  = "c(\'" + "\', \'".join(labels) + "\')"
    call  = r_name + " = " + "Venn(" + "Weight = " + weight_string + ", SetNames = " + lab + ", " + ven_kw + ")"
    print call
    ro.r(call)
    ro.r("plot(" + r_name + "," + plot_kw + ")")
    
    
    
