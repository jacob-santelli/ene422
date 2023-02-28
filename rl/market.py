import functools

import gymnasium
import numpy as np
from gymnasium.spaces import Discrete, Box
import pandas as pd

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

ROCK = 0
PAPER = 1
SCISSORS = 2
NONE = 3
MOVES = ["ROCK", "PAPER", "SCISSORS", "None"]
NUM_ITERS = 100
REWARD_MAP = {
    (ROCK, ROCK): (0, 0),
    (ROCK, PAPER): (-1, 1),
    (ROCK, SCISSORS): (1, -1),
    (PAPER, ROCK): (1, -1),
    (PAPER, PAPER): (0, 0),
    (PAPER, SCISSORS): (-1, 1),
    (SCISSORS, ROCK): (-1, 1),
    (SCISSORS, PAPER): (1, -1),
    (SCISSORS, SCISSORS): (0, 0),
}


def env(portfolios,demand_forecast, render_mode=None):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(portfolios=portfolios, demand_forecast=demand_forecast, render_mode=internal_render_mode)
    # This wrapper is only for environments which print results to the terminal
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv):
    """
    The metadata holds environment constants. From gymnasium, we inherit the "render_modes",
    metadata which specifies which modes can be put into the render() method.
    At least human mode should be supported.
    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {"render_modes": ["human"], "name": "rps_v2"}

    def __init__(self, portfolios, demand_forecast, render_mode=None):
        """
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces
        These attributes should not be changed after initialization.
        """
        self.possible_agents = ["Portfolio " + str(r) for r in range(1,8)]
        self.num_gens_per_port = [portfolios[portfolios['portfolio'] == i]['id'].count() for i in range(1,8)]
        self.agent_portfolio_dict = {str(i+1):portfolios[portfolios['portfolio'] == i+1] for i in range(len(self.possible_agents))}
        print(self.agent_portfolio_dict['1'])
        self.agent_gen_dict = {agent:gens for (agent, gens) in zip(self.possible_agents, self.num_gens_per_port)}
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )
        print(self.agent_name_mapping)
        self.portfolios = portfolios
        self.portfolios = self.portfolios[["portfolio", "id", "mw","fuel cost $/MWh","variable O&M $/MWh",'fixed O&M $']]

        self.min_capacity = portfolios['mw'].min()
        self.max_capacity = portfolios['mw'].max()
        self.num_portfolios = portfolios.count()
        self.global_min_portfolios = self.portfolios.min().min()
        self.global_max_portfolios = self.portfolios.max().max()
        self.min_portfolio = self.portfolios['portfolio'].min().min()
        self.max_portfolio = self.portfolios['portfolio'].max().max()
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        # [capacity, price]
        # self.low_arr = np.array([[self.min_capacity, 0.01, None]])
        # self.high_arr = np.array([[self.max_capacity, 500, None]])
        self.num_hours = 4
        self._action_spaces = {}
        self._test_arrs = {}
        for k,v in self.agent_gen_dict.items():
            # Set the possible action space per portfolio as a function of their total number of generators
            # Action space: R^4 => [capacity, price, portfolio, generating_onehot]
            loop_low = np.array([[self.min_capacity, 0.01, int(self.agent_name_mapping[k]+1), 1]])
            loop_high = np.array([[self.max_capacity, 500, int(self.agent_name_mapping[k]+1), 100]])
            low = np.array([np.repeat(loop_low, v*self.num_hours, axis=0)]).reshape(self.num_hours, v, 4)
            high = np.array([np.repeat(loop_high, v*self.num_hours, axis=0)]).reshape(self.num_hours, v, 4)
            self._action_spaces[k] = Box(low=low,high=high, shape=(self.num_hours, v, 4))

        self._observation_spaces = {
            agent: Box(low=self.global_min_portfolios, high=self.global_max_portfolios, shape=(self.portfolios.shape[0], self.portfolios.shape[1])) for agent in self.possible_agents
        }
        #print(self._action_spaces['Portfolio 1'])
        self.render_mode = render_mode
        self.round_data = {k:[] for k in self.possible_agents}
        self.demand_forecast = demand_forecast

    # this cache ensures that same space object is returned for the same agent
    # allows action space seeding to work as expected
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        return self._observation_spaces[agent]

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return self._action_spaces[agent]
    
    # Calculate revenue given supply curve, price, etc.
    def revenue(self, price, supply_curve, generators):
        pass

    def render(self):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        if self.render_mode is None:
            gymnasium.logger.warn(
                "You are calling render method without specifying any render mode."
            )
            return

        if len(self.agents) == 7:
            string = "Current state: Agent1: {} , Agent2: {}".format(
                MOVES[self.state[self.agents[0]]], MOVES[self.state[self.agents[1]]]
            )
        else:
            string = "Game over"
        print(string)

    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return np.array(self.observations[agent])

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass

    def reset(self, seed=None, return_info=False, options=None):
        """
        Reset needs to initialize the following attributes
        - agents
        - rewards
        - _cumulative_rewards
        - terminations
        - truncations
        - infos
        - agent_selection
        And must set up the environment so that render(), step(), and observe()
        can be called without issues.
        Here it sets up the state dictionary which is used by step() and the observations dictionary which is used by step() and observe()
        """
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.state = {agent: NONE for agent in self.agents}
        self.observations = {agent: NONE for agent in self.agents}
        self.num_moves = 0
        self.round_data = {k:[] for k in self.possible_agents}
        self.total_days = 0

        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

    def step(self, action):
        """
        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - terminations
        - truncations
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            # handles stepping an agent which is already dead
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next dead agent,  or if there are no more dead agents, to the next live agent
            self._was_dead_step(action)
            return

        if (
            self.total_days >= 6
        ):
            self._was_dead_step(action)
            return
        agent = self.agent_selection

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        self._cumulative_rewards[agent] = 0

        # stores action of current agent
        self.state[self.agent_selection] = action

        # collect reward if it is the last agent to act
        if self._agent_selector.is_last():

            day_supply_curves = {
                '1':[],
                '2':[],
                '3':[],
                '4':[]
            }
            # COLLECT ALL BIDDED SUPPLY AND ORDER BY PRICE
            for agent in self.possible_agents:
                agent_action_mat = self.state[agent]
                for hour in range(len(agent_action_mat)):
                    day_supply_curves[f'hr{hour+1}'].append(agent_action_mat[hour])

            for hr, supply_curve in day_supply_curves:
                sorted_supply = supply_curve.sort(key=lambda x: x[1], ascending=True)
                demand_mean = self.demand_forecast[self.total_days * 4 + (int(hr)-1)]
                demand = np.random.normal(loc = demand_mean, scale=0.03 * demand_mean)
                data_dict = {
                    'capacity':sorted_supply[:, 0],
                    'price':sorted_supply[:, 1], 
                    'portfolio':sorted_supply[:, 2],
                    'id':sorted_supply[:, 3]
                }
                df = pd.DataFrame(data_dict)
                df['cum_cap'] = df['capacity'].cumsum()


                df["is_generating"] = df["cum_cap"] < demand

                # Marginal generator - need to cover entire demand (perfectly inelastic), so add final generator
                marg_gen_index = df.loc[~df["is_generating"], :].index.values.tolist()[0]
                # (also set is_generating true for marg gen)
                df.loc[df.index == marg_gen_index, 'is_generating'] = 1
                # Hour price
                hour_price = df[df.index == marg_gen_index]['price']
                print(f'Hour price: {hour_price}')

                hour_slice = df.loc[df.is_generating, :]

                day_supply_curves[hr] = [hour_price, hour_slice]
                print(day_supply_curves[hr])


            # # rewards for all agents are placed in the .rewards dictionary
            # self.rewards[self.agents[0]], self.rewards[self.agents[1]] = REWARD_MAP[
            #     (self.state[self.agents[0]], self.state[self.agents[1]])
            # ]

            # self.num_moves += 1
            # # The truncations dictionary must be updated for all players.
            # self.truncations = {
            #     agent: self.num_moves >= NUM_ITERS for agent in self.agents
            # }

            # # observe the current state
            # for i in self.agents:
            #     self.observations[i] = self.state[
            #         self.agents[1 - self.agent_name_mapping[i]]
            #     ]
        else:
            # necessary so that observe() returns a reasonable observation at all times.
            self.state[self.agents[1 - self.agent_name_mapping[agent]]] = NONE
            # no rewards are allocated until both players give an action
            self._clear_rewards()

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()
        self.total_days += 1

        if self.render_mode == "human":
            self.render()