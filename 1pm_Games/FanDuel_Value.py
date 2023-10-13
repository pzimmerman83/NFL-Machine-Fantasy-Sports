import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Load your data into a Pandas DataFrame
df = pd.read_csv(r'C:\Users\patri\Desktop\Fantasy\1pm_Games\filtered_fanduel_data.csv')

# Define player positions
positions = ['QB', 'RB1', 'RB2', 'Flex', 'WR1', 'WR2', 'WR3', 'TE', 'D']

# Store the nine teams in a list
teams = []

for team_number in range(100): # Run the optimization process nine times to generate nine teams
    # Create an LP problem for the current team
    model = LpProblem(name=f"Fantasy_Football_Team_{team_number+1}", sense=LpMaximize)

    # Create binary variables for player selection for the current team
    player_vars = LpVariable.dicts(f"Player{team_number+1}", df.index, cat='Binary')

    # Objective functions
    objective_score = lpSum(df.loc[i, 'FPPG'] * player_vars[i] for i in df.index)

    # Add the name of the player you want to always include |player_to_include = "Christian McCaffrey"

    # Get the index of the player to include |player_index = df[df['Nickname'] == player_to_include].index[0]

    # Constraint: Always include the player_to_include | model += player_vars[player_index] == 1


    # Position constraints for the current team
    positions = ['QB', 'RB1', 'RB2', 'Flex', 'WR1', 'WR2', 'WR3', 'TE', 'D']
    for pos in positions:
        if pos == 'QB':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1

        elif pos == 'RB1':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1           
           
        elif pos == 'RB2':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1
           
        elif pos == 'Flex':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1
            
        elif pos == 'WR1':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 2

        elif pos == 'WR2':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1

        elif pos == 'WR3':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 0
            
        elif pos == 'D':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1
       
        elif pos == 'TE':
            model += lpSum(player_vars[i] for i in df.index if df.loc[i, 'Position'] == pos) == 1
          
    # Salary constraint: total salary <= 60,000 for the current team
    model += lpSum(df.loc[i, 'Salary'] * player_vars[i] for i in df.index) >= 58000
    model += lpSum(df.loc[i, 'Salary'] * player_vars[i] for i in df.index) <= 60000
        
   # Exclude the exact combination of players that form a team
    for prev_team in teams:
        model += lpSum(player_vars[i] for i in prev_team) <= len(prev_team) - 1

    # Solve the optimization problem for the current team
    model.solve()
   
    # Extract selected players for the current team
    selected_players = [i for i in df.index if player_vars[i].varValue == 1]

    # Add the selected team to the list of teams
    teams.append(selected_players)


    


# Create a list to store team data
team_data = []

for i, selected_players in enumerate(teams):
    selected_team = df.loc[selected_players, ['Id','Position', 'Nickname', 'Team', 'Salary', 'FPPG', 'Value','% Rostered']]
    # Join 'ID' & 'Nickname' with a ":"
    selected_team['ID_Nickname'] = selected_team.apply(lambda row: f"{row['Id']}:{row['Nickname']}", axis=1)
    total_salary = selected_team['Salary'].sum()
    total_fppg = selected_team['FPPG'].sum()
    team_data.append((selected_team, total_salary, total_fppg))
    
# Sort the teams by total FPPG in descending order
team_data.sort(key=lambda x: x[2], reverse=True)

# Display all teams, now sorted by FPPG
for i, (selected_team, total_salary, total_fppg) in enumerate(team_data):
    print(f"Team {i+1}:\n")
    print(selected_team)
    print(f"Total Salary: ${total_salary}")
    print(f"Total FPPG: {total_fppg}\n")

    # Export teams to Excel
with pd.ExcelWriter('teams.xlsx') as writer:
    for i, (selected_team, _, _) in enumerate(team_data):
        selected_team.to_excel(writer, sheet_name=f'Team {i+1}')


