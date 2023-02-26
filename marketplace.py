#!/usr/bin/env python3
#--------------------------------------------
# marketplace.py
# Author: Jacob Santelli and Ian Murphy
#--------------------------------------------

import pandas as pd

# takes a list of portfolio panda objects, returns them appended to one another
def append(portList):
  df = portList[0]
  for port in portList[1:]: {
      df.append(port)
  }
  return df

def portSort(portFrame):
  portFrame.sort_values('price')
  