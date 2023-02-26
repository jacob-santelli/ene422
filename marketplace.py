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
    data['price'] = [np.random.randint(5)]* len(data)

    simulate_hour(10, data)

    
def sample_demand(mu, sd=0.03):
  return np.random.normal(loc = mu, scale = sd)

def set_price_by_id(data, id, price):
    data_copy = data.copy()
    data_copy.loc[data_copy['id'] == id, ('price')] = price
    return data_copy

def get_ids_of_portfolios(data, portfolio):
   data_copy = data.copy()
   return data_copy.loc[data_copy['portfolio'] == portfolio, ('id')]

def simulate_hour(mean_demand, generator_data):
  sampled_demand = sample_demand(mean_demand)
  data_copy = generator_data.copy()
  data_copy['revenue'] = 0

  # Sort data by price
  data_copy.sort_values('price', ascending=True, inplace=True)

  # Get cumulative demand
  data_copy['cumulative_capacity'] = data_copy.loc[:, ('mw')].cumsum()

  print(data_copy.head())

def sandbox():
   df = pd.DataFrame()


if __name__ == "__main__":
  main()
  