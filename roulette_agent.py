import numpy as np


class RouletteAgent:
    """
    Class to simulate Roulette agent
    """
    def __init__(
        self,
        init_budget: int,
        consecutive_threshold: int,
        echo: bool = False,
        # bet_amount: int
    ):
        self.budget = init_budget
        self.consecutive_threshold = consecutive_threshold
        self.bet_amount = 0
        self.bet_count = 0
        self.consecutive_count = 0
        self.budget_history = []
        self.previous_outcome = ""
        self.bet_content = "NO BET"
        self.should_bet = False
        self.echo = echo

    def get_budget_history(self) -> list:
        """
        Return budget history
        :return: return self.budget_history
        """
        return self.budget_history

    def bet(self, bet_amount: int):
        """
        Update budget and bet count
        :param bet_amount: bet amount

        """
        if self.budget >= bet_amount:
            self.budget -= bet_amount
        self.bet_amount = bet_amount
        self.bet_count += 1
        if self.echo:
            print(f"Bet: {self.bet_content} - {bet_amount}")
        self.should_bet = False

    def observe(self, index: int, current_outcome: str):
        """
        Observe and adjust given current outcome
        :param index: index of spin
        :param current_outcome: current outcome
        """
        # If first round, move on
        if index == 0:
            self.previous_outcome = current_outcome
            return

        # Check if hit
        if self.bet_content == current_outcome:
            if self.echo:
                print("Hit!")
            self.budget += (self.bet_amount * 2)
        self.bet_content = "NO BET"

        # Check consecutive count
        if current_outcome == self.previous_outcome:
            self.consecutive_count += 1
        else:
            self.consecutive_count = 0

        # Check if should bet after seeing current outcome
        if self.consecutive_count >= self.consecutive_threshold:
            self.should_bet = True
            if current_outcome == "R":
                self.bet_content = "B"
            elif current_outcome == "B":
                self.bet_content = "R"
        else:
            self.bet_content = "NO BET"

        self.previous_outcome = current_outcome
        self.budget_history.append(self.budget)

    def play(self, result_dict: dict, bet_amount):
        """
        Play function
        :param result_dict: input result dictionary
        :param bet_amount: bet amount
        :return:
        """
        color = result_dict['color']
        index = result_dict['index']
        self.observe(index=index, current_outcome=color)
        if self.should_bet:
            self.bet(bet_amount=bet_amount)
        if self.echo:
            print(100 * '-')




