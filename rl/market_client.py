import market
import pandas as pd
import numpy as np


def main():
    portfolios = pd.read_csv('Portfolios-2.csv')
    print(portfolios[portfolios['portfolioname']=='Bay_Views'])
    demand = pd.read_csv('demand_curve.csv', thousands=',')
    all_demand = demand['load']
    market.env(portfolios=portfolios, demand_forecast=all_demand)

if __name__ == "__main__":
    main()