import pandas as pd

# Load your player data from a CSV file
df = pd.read_csv(r'C:\Users\patri\Desktop\Fantasy\1pm_Games\FanDuel.csv')

# Remove unnecessary columns
columns_to_remove = ['First Name', 'Last Name', 'Game', 'Tier', 'Roster Position', 'Unnamed: 14', 'Unnamed: 15']
df = df.drop(columns=columns_to_remove)

# Filter out rows with non-null 'Injury Indicator'
df = df[df['Injury Indicator'].isnull()]

# List of player nicknames to exclude
nicknames_to_exclude = ['Andy Dalton', 'Trey Lance']

# Filter out rows where 'Nickname' is not in the list of nicknames to exclude
df = df[~df['Nickname'].isin(nicknames_to_exclude)]

# Remove rows with 0, NaN, or negative 'FPPG' values
df = df[df['FPPG'] > 0]

# Load the additional data you want to join with your existing DataFrame
other_df = pd.read_csv(r'C:\Users\patri\Desktop\Fantasy\Defense_Rank.csv')

# Perform a left join on the 'Opponent' column
df = df.merge(other_df[['Opponent', 'D_Val']], on='Opponent', how='left')

# Load the Percent_Rostered data
percent_rostered_df = pd.read_csv(r'C:\Users\patri\Desktop\Fantasy\Percent_Rostered.csv')

# Perform a left join on the 'Nickname' column to add the '% Rostered' column
df = df.merge(percent_rostered_df, on='Nickname', how='left')

# Load the additional data you want to join with your existing DataFrame
offensive_rank_df = pd.read_csv(r'C:\Users\patri\Desktop\Fantasy\Offensive_Rank.csv')

# Perform a left join on the 'Team' column to add the 'O_Val' column
df = df.merge(offensive_rank_df[['Team', 'O_Val']], on='Team', how='left')

# Define a function for custom computation (e.g., Value calculation)
def custom_computation(row):
    result = row['FPPG'] / row['Salary']* row['D_Val'] + row['O_Val']
    return result

# Use the assign() method to add the new column
df = df.assign(Value=df.apply(custom_computation, axis=1))

# Remove rows with 0, NaN, or negative 'FPPG' values
df = df[df['% Rostered'] > 10]

# Sort the DataFrame by 'Value' column in descending order
df = df.sort_values(by='Value', ascending=False)

#ReAssign Positions 

def assign_role(row):
    if row['Position'] == 'RB':
        if 18 <= row['FPPG'] <= 50:
            return 'RB1'
        elif 10 <= row['FPPG'] < 18:
            return 'RB2'
        else:
            return 'Flex'
    elif row['Position'] == 'WR':
        if 18 <= row['FPPG'] <= 50:
            return 'WR1'
        elif 12 <= row['FPPG'] < 18:
            return 'WR2'
        elif 8 <= row['FPPG'] < 12:
            return 'WR3'
        else:
            return 'Flex'
    else:
        return row['Position']

df['Position'] = df.apply(assign_role, axis=1)


# Export the sorted DataFrame to a CSV file
export_path = r'C:\Users\patri\Desktop\Fantasy\1pm_Games\filtered_fanduel_data.csv'
df.to_csv(export_path, index=False)

print(f"Filtered data exported to {export_path}")
