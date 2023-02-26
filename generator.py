#!/usr/bin/env python3
#--------------------------------------------
# generator.py
# Author: Jacob Santelli and Ian Murray
#--------------------------------------------
class Generator:
  def __init__(self, gentype, capacity, fixom, varom, fuel_cost):
    self.gentype = gentype
    self.capacity = capacity
    self.fixom = fixom
    self.varom = varom
    self.fuel_cost = fuel_cost

    # marginal costs of production
    self.marginal_cost = self.fuel_cost + self.varom

  def getCapacity(self):
    return self.capacity