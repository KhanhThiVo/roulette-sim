import random
import pandas as pd
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import plotly.express as px

roulette_numbers_ordered_corrected = [
    '00G', '28B', '09R', '26B', '30R', '11B', '07R', '20B', '32R', '17B', '05R','22B', '34R', '15B', '03R', '24B',
    '36R', '13B', '01R',
    '37G', '27R', '10B', '25R', '29B', '12R', '08B', '19R', '31B', '18R', '06B', '21R', '33B','16R', '04B', '23R',
    '35B', '14R', '02B'
]
# def spin_roulette_wheel():
#     results =[]
#     for i in range(1,1001):
#         result = random.choice(roulette_numbers_ordered_corrected)
#         number = int(''.join(filter(str.isdigit, result)))
#         color = ''.join(filter(str.isalpha, result))
#         results.append({
#         'Index': i,
#         'Result': result,
#         'Number': number,
#         'Letter': color
#         })
#     df = pd.DataFrame(results)
#     return df

def generate_random_choice(index):
    result = random.choice(roulette_numbers_ordered_corrected)
    number = int(''.join(filter(str.isdigit, result)))
    color = ''.join(filter(str.isalpha, result))

    return {
        'index': index,
        'result': result,
        'number': number,
        'color': color
    }
#
# def spin_roulette_wheel_parallel(n):
#     # Use Parallel to generate random choices in parallel
#     results = Parallel(n_jobs=-1)(delayed(generate_random_choice)(i) for i in range(1, n+1))
#
#     df = pd.DataFrame(results)
#     return df
#
# df=spin_roulette_wheel_parallel(50000000)
#
# plt.hist(df['color'], bins='auto', alpha=0.7, rwidth=0.85)
# plt.title('Distribution of Numbers in Roulette Wheel Simulation')
# plt.xlabel('Number')
# plt.ylabel('Frequency')
# plt.show()



def spin_roulette_wheel_parallel(initial_budget, bet_amount, consecutive_threshold, spins):
    budget = initial_budget
    consecutive_count = 0
    budget_history= []
    print(f"Initial budget: {initial_budget}")
    bet = 0
    spin_count = 0
    bet_count = 0
    results = Parallel(n_jobs=-1)(delayed(generate_random_choice)(i) for i in range(1, spins + 1))

    for index, result_dict in enumerate(results):
        spin_count += 1
        print(f"SpinCount: {spin_count}")
        print(f"Bet Count: {bet_count}")
        result = result_dict['color']
        print(f"RESULT {result}")
        if index == 0:
            result_to_check = result
        if index != 0 :
            print(f"BET: {bet}")
            if bet == result:
                print(bet == result)
                budget = budget + (bet_amount * 2)
            print(f"Budget: {budget}")


            print(f"Previous result {result_to_check}")
            if result == result_to_check:
                consecutive_count += 1
            else:
                consecutive_count = 0
            print(f"Consecutive {consecutive_count}")
            result_to_check = result
            if (consecutive_count == consecutive_threshold or consecutive_count > consecutive_threshold) \
                    and  consecutive_count <= 4 and budget >= bet_amount:
                budget -= bet_amount
                bet_count +=1
                if result == "R":
                    bet = "B"
                elif result =="B":
                    bet = "R"
            else:
                bet = "NO BET"
            budget_history.append(budget)

        print(100 * "-")
    return budget_history

# Set the parameters
initial_budget = 50
bet_amount = 5
consecutive_threshold = 2
spins = 1000

# Run the simulation
budget_history = spin_roulette_wheel_parallel(initial_budget, bet_amount, consecutive_threshold, spins)

# Visualize the results with Matplotlib
fig = px.line(x=range(1, len(budget_history) + 1), y=budget_history, labels={'x': 'Round', 'y': 'Budget'},
              title='Roulette Wheel Simulation with Betting',
              line_shape='linear')

fig.update_layout(xaxis_title='Round', yaxis_title='Budget', legend_title='Legend')
fig.show()



