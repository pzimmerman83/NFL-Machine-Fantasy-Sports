import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from math import sqrt
import tkinter as tk
from tkinter import messagebox


# Load your data
offensive_df = pd.read_csv(r'C:\Users\patri\Desktop\Fantasy\Predictive\Basic_Stats_Off.csv')
defensive_df = pd.read_csv(r'C:\Users\patri\Desktop\Fantasy\Predictive\Basic_Stats_Def.csv')

# Merge the two dataframes
df = pd.merge(offensive_df, defensive_df, on='Team')

# Calculate net offensive statistics by subtracting opponent's defensive statistics
net_offense = df[['Off_Pass_Yds', 'Off_Rush_Yds', 'Off_Rsh_TD', 'Off_Rec_TD', 'Off_Pass_Att', 'Off_Pass_Cmp', 'Off_Rush_Att', 'Off_Rush_YPC']].values - df[['Def_PassYds_Allowed', 'RushYds_Allowed', 'Def_Pass_TD_Allowed', 'Def_Rush_TD_Allowed', 'Def_Pass_Att', 'Def_Pass_Cmp', 'Def_Rush_Att', 'Def_Rush_YPC']].values


df['Net_Off_Pass_Yds'] = net_offense[:, 0]
df['Net_Off_Rush_Yds'] = net_offense[:, 1]
df['Net_Off_Rsh_TD'] = net_offense[:, 2]
df['Net_Off_Rec_TD'] = net_offense[:, 3]
df['Net_Off_Pass_Att'] = net_offense[:, 4]
df['Net_Off_Pass_Cmp'] = net_offense[:, 5]
df['Net_Off_Rush_Att'] = net_offense[:, 6]
df['Net_Off_Rush_YPC'] = net_offense[:, 7]

# Define features based on net offensive statistics
features = [
    'Net_Off_Pass_Yds', 'Net_Off_Rush_Yds', 'Net_Off_Rsh_TD', 'Net_Off_Rec_TD','Net_Off_Pass_Att', 'Net_Off_Pass_Cmp', 'Net_Off_Rush_Att', 'Net_Off_Rush_YPC',
    'Def_PassYds_Allowed', 'RushYds_Allowed', 'Def_Pass_TD_Allowed', 'Def_Rush_Att', 'Def_Rush_YPC',
    'Def_Rush_TD_Allowed', 'Def_Tot_Allowed','Def_Pass_Att', 'Def_Pass_Cmp'
]

X = df[features]
y = df['Off_Tot_TD']

# Data splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define your pipeline
pipeline = make_pipeline(StandardScaler(), LinearRegression())

# Fit and transform your training data
pipeline.fit(X_train, y_train)

# Transform your testing data and make predictions
y_pred = pipeline.predict(X_test)

# Model evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Calculate RMSE
rmse = sqrt(mse)
print(f"Root Mean Squared Error: {rmse}")

# Calculate MAE
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Let's say Team A is 'Chiefs' and Team B is 'Broncos'
team_A_name = 'Cowboys'
team_B_name = 'Rams'

# Extract data for Team A and Team B
team_A_data = df[df['Team'] == team_A_name][features]
team_B_data = df[df['Team'] == team_B_name][features]

# Make predictions for Team A and Team B using the pipeline
team_A_prediction = pipeline.predict(team_A_data)
team_B_prediction = pipeline.predict(team_B_data)

# Print the projected scores
print(f"Projected Score for {team_A_name}: {team_A_prediction[0]}")
print(f"Projected Score for {team_B_name}: {team_B_prediction[0]}")

# Determine and print the winner
if team_A_prediction > team_B_prediction:
    print(f"{team_A_name} is predicted to win.")
elif team_B_prediction > team_A_prediction:
    print(f"{team_B_name} is predicted to win.")
else:
    print("The game is predicted to be a tie.")
