#!/usr/bin/env python3
# --------------------------------------------
# marketplace.py
# Author: Jacob Santelli and Ian Murray
# --------------------------------------------

import pandas as pd
import numpy as np


# takes a list of portfolio panda objects, returns them appended to one another
def append(portList):
    df = portList[0]
    for port in portList[1:]:
        {df.append(port)}
    return df


def portSort(portFrame):
    portFrame.sort_values("price")


def sampleDemand(mean_demand, sd=0.03):
    pass


def calcRevenue(df, price):
  df['revenue'] = df['is_generating'] * \
   (df['mw'] * \
   (price - \
    df['fuelcost'] - df['varom'] - df['carbon']))
    

# ------------ SINGLE ITERATION ---------------
# 1. Portfolios send prices
# 2. All supply sorted and creates supply curve
# 3. Demand sampled and inelastic demand intersects with supply curve at marginal price
# 4. For generating plants, return money back to portfolio based on supply they satisfied and inframarginal rents


def main():
    portfolios_data = pd.read_csv("./generator_info.csv")

    portfolios_data["is_generating"] = False
    portfolios_data["price"] = np.random.randint(1, 6, size=portfolios_data.shape[0])

    simulate_hour(10800, portfolios_data)


def sample_demand(mu, sd=0.03):
    return np.random.normal(loc=mu, scale=sd)


def set_price_by_id(data, id, price):
    data_copy = data.copy()
    data_copy.loc[data_copy["id"] == id, ("price")] = price
    return data_copy


def get_ids_of_portfolios(data, portfolio):
    data_copy = data.copy()
    return data_copy.loc[data_copy["portfolio"] == portfolio, ("id")]


def simulate_hour(mean_demand, generator_data):
    sampled_demand = sample_demand(mean_demand)
    data_copy = generator_data.copy()
    data_copy["revenue"] = 0

    # Sort data by price
    data_copy.sort_values("price", ascending=True, inplace=True)

    # Get cumulative demand
    # data_copy['cumulative_capacity'] = data_copy.loc[:, ('mw')].cumsum()

    templist = data_copy.loc[:, ("mw")].cumsum()
    data_copy["cumulative_capacity"] = templist

    print(f"Pre: {data_copy.shape}")
    # Get energy price for this hour
    data_copy["is_generating"] = data_copy["cumulative_capacity"] < sampled_demand
    print(f"Post: {data_copy.shape}")

    # Marginal generator - need to cover entire demand, so add final generator
    marg_gen = data_copy[~data_copy["is_generating"]].iloc[0]

    print(f"Sampled demand: {sampled_demand}")
    print(marg_gen)
    print(data_copy[data_copy["is_generating"]].iloc[-1])


def sandbox():
    df = pd.DataFrame()

    portfolio_1 = {"X": 69.00, "Y": 500.00}
    # price of generating unit with ID X from portfolio 1
    portfolio_1["X"]

# set all of the generators from portfolio port
# to a price defined by some arbitrary function
# price_func by passing all relevant parameters
def set_portfolio_prices(data, price_func, port):
  data_copy = data.copy()
  list_of_ids = get_ids_of_portfolios(data_copy, port)

  for id in data_copy:
    if id in list_of_ids:
      data_copy[data_copy['id'] == id]['price'] = \
      price_func(data_copy[data_copy['id'] == id]['mw'],
                 data_copy[data_copy['id'] == id]['varom'],
                 data_copy[data_copy['id'] == id]['carbon'],
                 data_copy[data_copy['id'] == id]['varom'],
                 data_copy[data_copy['id'] == id]['fixom'],
                 )
      
  



if __name__ == "__main__":
    main()
