#!/usr/bin/env python3
#--------------------------------------------
# marketplace.py
# Author: Jacob Santelli and Ian Murray
#--------------------------------------------

import pandas as pd
import numpy as np

# takes a list of portfolio panda objects, returns them appended to one another
def append(portList):
  df = portList[0]
  for port in portList[1:]: {
      df.append(port)
  }
  return df

def portSort(portFrame):
  portFrame.sort_values('price')

def sampleDemand(mean_demand, sd = 0.03):
  pass

# ------------ SINGLE ITERATION ---------------
# 1. Portfolios send prices
# 2. All supply sorted and creates supply curve
# 3. Demand sampled and inelastic demand intersects with supply curve at marginal price
# 4. For generating plants, return money back to portfolio based on supply they satisfied and inframarginal rents


def main():

    data = pd.read_csv("./Portfolios-2.csv")

    data['is_generating'] = False
    data['price'] = 0

    # gimme port 1
    data[data['portfolio'] == 3].loc[:, ('price')]= 1
    print(data[data['portfolio'] == 3])

    

if __name__ == "__main__":
  main()
  