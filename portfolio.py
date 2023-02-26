#!/usr/bin/env python3
#--------------------------------------------
# portfolio.py
# Author: Jacob Santelli and Ian Murphy
#--------------------------------------------

import pandas as pd




class Portfolio:
  def __init__(self, listGen):
    columns = {'self', 'portfolio', 'portfolioname', 
               'name', 'id', 'location', 'mw', 'fuelcost', 'varom', 'fixom',
               'carbon', 'resource', 'marginal'}
    df = pd.DataFrame(columns= columns)
    for gen in listGen: {
        df.append(gen)
    }
    
    # add two more columns to portfolio dataframe
    boolList =  [False for i in range(len(listGen))]
    priceList = [0 for i in range(len(listGen))]
    df['is_generating'] = boolList
    df['price'] = priceList

