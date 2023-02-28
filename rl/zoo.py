import numpy as np
from pettingzoo import AECEnv, ParallelEnv
from pettingzoo.utils import agent_selector, wrappers
from pettingzoo.utils.conversions import parallel_wrapper_fn

# Define a class for the marketplace environment
class MarketEnv(AECEnv):
    def __init__(self, num_players, num_generators, demand, interest_rate, price_weight):
        super().__init__()
        self.num_players = num_players
        self.num_generators = num_generators
        self.demand = demand
        self.interest_rate = interest_rate
        self.price_weight = price_weight
        self.players = []
        self.market_price = None
        
    def add_player(self, player):
        self.players.append(player)
        
    def generate_demand(self):
        # Generate random demand from a normal distribution
        demand = np.random.normal(loc=self.demand, scale=10, size=self.num_generators)
        demand = np.clip(demand, 0, np.inf)
        return demand
        
    def intersect_supply_demand(self, supply, demand):
        # Sort supply by price
        supply = sorted(supply, key=lambda x: x[1])
        intersected = []
        remaining_demand = demand
        for s in supply:
            if s[0] <= remaining_demand:
                intersected.append((s[0], s[1]))
                remaining_demand -= s[0]
            else:
                intersected.append((remaining_demand, s[1]))
                remaining_demand = 0
                break
        return intersected, remaining_demand
        
    def observe(self, agent):
        # Construct the observation for the given agent
        player_idx = self.players.index(agent)
        observation = []
        for i in range(self.num_generators):
            observation.append(self.players[player_idx].generators[i].capacity)
            observation.append(self.players[player_idx].generators[i].price)
        observation.append(self.market_price)
        return observation
        
    def step(self, action):
        # Update the state based on the given actions
        supply = []
        for player in self.players:
            for generator in player.generators:
                supply.append((generator.capacity, generator.price))
        demand = self.generate_demand()
        intersected, remaining_demand = self.intersect_supply_demand(supply, demand)
        self.market_price = np.sum([s[1] for s in intersected])/np.sum([s[0] for s in intersected]) if intersected else 0
        rewards = {}
        for player in self.players:
            rewards[player] = -player.calculate_loan_interest(self.interest_rate)
            for generator in player.generators:
                if (generator.capacity, generator.price) in intersected:
                    rewards[player] += self.market_price * generator.capacity - generator.calculate_cost()
        for player, action in zip(self.players, action):
            player.update_prices(action)
        done = {"__all__": False}
        return self.observe(self.players[0]), rewards, done, {}
    
    def reset(self):
        # Reset the environment state
        self.market_price = None
        for player in self.players:
            player.reset_prices()
        return self.observe(self.players[0])

# Define a class for the player agent
class PlayerAgent:
    def __init__(self, id, num_generators):
        self.id = id
        self.generators = []
        for i in range(num_generators):
            self.generators.append(Generator())
        self

    def update_prices(self, prices):
        # Update the prices for each generator
        for i in range(len(prices)):
            self.generators[i].price = prices[i]
        
    def reset_prices(self):
        # Reset the prices for each generator to a default value
        for generator in self.generators:
            generator.price = 10
        
    def calculate_loan_interest(self, interest_rate):
        # Calculate the interest on the player's loan
        loan = np.sum([generator.cost for generator in self.generators])
        return loan * (interest_rate/365)
    
# Define a class for the generator
class Generator:
    def __init__(self):
        self.capacity = np.random.randint(low=1, high=11) * 10
        self.cost = np.random.randint(low=1, high=11) * 10
        self.price = 10
        
    def calculate_cost(self):
        # Calculate the cost of generating energy
        return self.capacity * self.cost
        
# Define a wrapper function to convert the environment to a parallel environment
def parallel_env(env_creator_fn, **kwargs):
    env = env_creator_fn(**kwargs)
    env = wrappers.ClipOutOfBoundsWrapper(env)
    env = wrappers.NanNoOpWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env

# Define a function to create the environment
def create_env():
    env = MarketEnv(num_players=7, num_generators=3, demand=200, interest_rate=0.05, price_weight=0.1)
    players = []
    for i in range(env.num_players):
        players.append(PlayerAgent(id=i, num_generators=env.num_generators))
    for player in players:
        env.add_player(player)
    return env

# Create a parallel environment with 7 agents and 1 market
parallel_env_fn = parallel_wrapper_fn(create_env)
parallel_env = ParallelEnv()
