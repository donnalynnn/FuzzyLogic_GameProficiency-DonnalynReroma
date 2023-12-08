import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


def calculate_rank():
    wins_value = int(input("Enter the number of wins: "))
    games_played_value = int(input("Enter the number of games played: "))

    rank_sim.input['wins'] = wins_value
    rank_sim.input['games_played'] = games_played_value

    # Compute the result
    rank_sim.compute()

     # Get the fuzzy result
    fuzzy_result = rank_sim.output['rank']

    # Check if the result is within the valid range
    if 0 <= fuzzy_result <= 100:
        # Define a custom mapping from numeric result to words
        rank_words_mapping = {
            (0, 20): 'The Happy Noob',
            (20, 40): 'The Determined Rookie',
            (40, 60): 'The Hungry Veteran',
            (60, 80): 'Evil Warlord',
            (80, 100): 'Gamer Utopia',
            (60, 80): 'Gamer Burn Out'
        }

        # Find the corresponding word based on the numeric result
        result_word = next(word for (lower, upper), word in rank_words_mapping.items() if lower <= fuzzy_result <= upper)

        print(f"Player's Rank (Numeric): {fuzzy_result}")
        print(f"Player's Rank (Word): {result_word}")
    else:
        print("Invalid result. Please check your input values.")
        
        
    # Visualize the fuzzy membership functions and rules
    wins.view()
    games_played.view()
    rank.view(sim=rank_sim)
    plt.show()

# Create Antecedents and Consequent
wins = ctrl.Antecedent(np.arange(0, 101, 1), 'wins')
games_played = ctrl.Antecedent(np.arange(0, 101, 1), 'games_played')
rank = ctrl.Consequent(np.arange(0, 101, 1), 'rank')

# Define membership functions
wins['low'] = fuzz.trimf(wins.universe, [0, 0, 50])
wins['medium'] = fuzz.trimf(wins.universe, [0, 50, 100])
wins['high'] = fuzz.trimf(wins.universe, [50, 100, 100])

games_played['low'] = fuzz.trimf(games_played.universe, [0, 0, 50])
games_played['medium'] = fuzz.trimf(games_played.universe, [0, 50, 100])
games_played['high'] = fuzz.trimf(games_played.universe, [50, 100, 100])

rank['Noob'] = fuzz.trimf(rank.universe, [0, 0, 20])
rank['Rookie'] = fuzz.trimf(rank.universe, [0, 20, 40])
rank['Veteran'] = fuzz.trimf(rank.universe, [20, 40, 60])
rank['Warlord'] = fuzz.trimf(rank.universe, [40, 60, 80])
rank['BurnOut'] = fuzz.trimf(rank.universe, [60, 80, 100])
rank['Utopia'] = fuzz.trimf(rank.universe, [80, 100, 100])

# Define rules
rule1 = ctrl.Rule(wins['low'] & games_played['low'], rank['Noob'])
rule2 = ctrl.Rule(wins['medium'] & games_played['low'], rank['Rookie'])
rule3 = ctrl.Rule(wins['high'] & games_played['low'], rank['Veteran'])
rule4 = ctrl.Rule(wins['low'] & games_played['medium'], rank['Noob'])
rule5 = ctrl.Rule(wins['medium'] & games_played['medium'], rank['Warlord'])
rule6 = ctrl.Rule(wins['high'] & games_played['medium'], rank['BurnOut'])
rule7 = ctrl.Rule(wins['low'] & games_played['high'], rank['Rookie'])
rule8 = ctrl.Rule(wins['medium'] & games_played['high'], rank['BurnOut'])
rule9 = ctrl.Rule(wins['high'] & games_played['high'], rank['Utopia'])

# Create control system
rank_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
rank_sim = ctrl.ControlSystemSimulation(rank_ctrl)

while True:
    print("===== Fuzzy Rank Calculator Menu =====")
    print("1. Calculate Rank")
    print("2. Exit")

    choice = input("Enter your choice (1-2): ")

    if choice == '1':
        calculate_rank()
    elif choice == '2':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1 or 2.")




