#!/usr/bin/env python3
#--------------------------------------------
# generator.py
# Author: Jacob Santelli and Ian Murray
#--------------------------------------------
class Generator:
  def __init__(self, portfolio, portfolioname, 
               name, id, location, mw, fuelcost, varom, fixom,
               carbon, resource, marginal):
    self.portfolio = portfolio
    self.portfolioname = portfolioname
    self.name = name
    self.id = id
    self.location = location
    self.mw = mw
    self.fuelcost = fuelcost
    self.varom = varom
    self.fixom = fixom
    self.carbon = carbon
    self.resource = resource
    self.marginal = marginal

    # marginal costs of production
    self.total_marginal = self.fuel_cost + self.varom + self.carbon

  def getCapacity(self):
    return self.capacity