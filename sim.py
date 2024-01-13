import random
import pandas as pd
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import plotly.express as px

from roulette_agent import RouletteAgent


class RouletteSim:
    """
    Class to simulate Roulette table
    """
    def __init__(self, wheel: list, n_spins: int, agent: RouletteAgent, bet_amount: int):
        self.wheel = wheel
        self.agent = agent
        self.n_spins = n_spins
        self.bet_amount = bet_amount
        self.final_budget = -1

    def generate_random_choice(self, index) -> dict:
        """
        Generate random choice from wheel
        :param index: index of spin
        :return: result of spin as dict
        """
        result = random.choice(self.wheel)
        number = int(result[:-1])
        color = result[-1]

        return {
            'index': index,
            'result': result,
            'number': number,
            'color': color
        }

    def spin_roulette_wheel_parallel(self):
        """
        Run simulation roulette spins
        :return:
        """
        results = Parallel(n_jobs=-1)(delayed(self.generate_random_choice)(i) for i in range(1, self.n_spins + 1))

        for index, result_dict in enumerate(results):
            self.agent.play(result_dict=result_dict, bet_amount=self.bet_amount)

        print(f"{self.n_spins} over")
        budget_history = self.agent.get_budget_history()

        self.final_budget = budget_history[-1]

    def plot_budget_history(self):
        """
        Plot budget history of agent
        """
        budget_history = self.agent.get_budget_history()
        # Visualize the results with Matplotlib
        fig = px.line(x=range(1, len(budget_history) + 1), y=budget_history, labels={'x': 'Round', 'y': 'Budget'},
                      title='Roulette Wheel Simulation with Betting',
                      line_shape='linear')

        fig.update_layout(xaxis_title='Round', yaxis_title='Budget', legend_title='Legend')
        fig.show()

    def get_final_budget(self):
        """
        Return remaining budget
        :return: self.final_budget
        """
        return self.final_budget


def sim_roulette(echo: bool = False):
    """
    Run roulette simulation
    :return: final budget of  run
    """
    initial_budget = 50
    bet_amount = 5
    consecutive_threshold = 2
    agent = RouletteAgent(
        init_budget=initial_budget,
        consecutive_threshold=consecutive_threshold,
        echo=echo,
    )

    spins = 1000
    roulette_numbers_ordered_corrected = [
        '00G', '28B', '09R', '26B', '30R', '11B', '07R', '20B', '32R', '17B', '05R', '22B', '34R', '15B', '03R', '24B',
        '36R', '13B', '01R',
        '37G', '27R', '10B', '25R', '29B', '12R', '08B', '19R', '31B', '18R', '06B', '21R', '33B', '16R', '04B', '23R',
        '35B', '14R', '02B'
    ]
    roulette_sim = RouletteSim(
        wheel=roulette_numbers_ordered_corrected,
        n_spins=spins,
        agent=agent,
        bet_amount=bet_amount
    )

    # Run sim
    roulette_sim.spin_roulette_wheel_parallel()

    # Plot budget history, uncomment if needed
    # roulette_sim.plot_budget_history()
    remaining_budget = roulette_sim.get_final_budget()
    print(f"Remaining budget: {remaining_budget}")

    return remaining_budget


if __name__ == '__main__':
    n_simulations = 10
    final_budgets = []
    for s in range(n_simulations):
        fb = sim_roulette()
        final_budgets.append(fb)
    plt.plot(final_budgets)
    plt.show()




