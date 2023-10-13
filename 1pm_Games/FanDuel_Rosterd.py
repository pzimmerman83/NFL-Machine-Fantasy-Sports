import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Load your data into a Pandas DataFrame
df = pd.read_csv(r'C:\Users\patri\Desktop\Fantasy\1pm_Games\filtered_fanduel_data.csv')

# Define player positions
positions = ['QB', 'RB', 'WR', 'TE', 'D']

# Store the nine teams in a list
teams = []

for team_number in range(9):  # Run the optimization process nine times to generate nine teams
    # Create an LP problem for the current team
    model = LpProblem(name=f"Fantasy_Football_Team_{team_number+1}", sense=LpMaximize)

    # Create binary variables for player selection for the current team
    player_vars = LpVariable.dicts(f"Player{team_number+1}", df.index, cat='Binary')

    # Objective functions
    objective_score = lpSum(df.loc[i, 'FPPG'] * player_vars[i] for i in df.index)
    
    # Salary constraint: total salary <= 60,000 for the current team
    model += lpSum(df.loc[i, 'Salary'] * player_vars[i] for i in df.index) >= 55000
    model += lpSum(df.loc[i, 'Salary'] * player_vars[i] for i in df.index) <= 60000

    # Position constraints for the current team
    for pos in positions:
        if pos == 'QB':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1
        elif pos == 'D':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1
        elif pos == 'TE':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1
        else:
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 3

    # Exclude the players selected for the previous teams in the current team's constraints
    for prev_team in teams:
        for player_index in prev_team:
            model += player_vars[player_index] == 0

    # Solve the optimization problem for the current team
    model.solve()

    # Extract selected players for the current team
    selected_players = [i for i in df.index if player_vars[i].varValue == 1]

    # Add the selected team to the list of teams
    teams.append(selected_players)

# Display all nine generated teams
for i, selected_players in enumerate(teams):
    print(f"Team {i+1}:\n")
    selected_team = df.loc[selected_players, ['Nickname', 'Position', 'Salary', 'FPPG', 'Value','% Rostered']]
    print(selected_team)
    print("\n")
