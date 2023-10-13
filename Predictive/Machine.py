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


# Define the function to be called when the Predict button is clicked
def predict():
    team_A_name = team_A_entry.get()
    team_B_name = team_B_entry.get()

    # Extract data for Team A and Team B
    team_A_data = df[df['Team'] == team_A_name][features]
    team_B_data = df[df['Team'] == team_B_name][features]

    # Make predictions for Team A and Team B using the pipeline
    team_A_prediction = pipeline.predict(team_A_data)
    team_B_prediction = pipeline.predict(team_B_data)

    # Determine the winner
    if team_A_prediction > team_B_prediction:
        winner = f"{team_A_name} is predicted to win."
    elif team_B_prediction > team_A_prediction:
        winner = f"{team_B_name} is predicted to win."
    else:
        winner = "The game is predicted to be a tie."

    messagebox.showinfo("Prediction Result", winner)

# Create a tkinter window
root = tk.Tk()

# Create and pack widgets for entering the names of Team A and Team B
team_A_label = tk.Label(root, text="Team A")
team_A_label.pack()
team_A_entry = tk.Entry(root)
team_A_entry.pack()

team_B_label = tk.Label(root, text="Team B")
team_B_label.pack()
team_B_entry = tk.Entry(root)
team_B_entry.pack()

# Create and pack the Predict button
predict_button = tk.Button(root, text="Predict", command=predict)
predict_button.pack()

# Start the tkinter event loop
root.mainloop()

# ... (Your existing code for loading data, defining features, splitting data, defining pipeline, fitting model, etc.)

# Define the function to be called when the Predict button is clicked
def predict():
    team_A_name = team_A_entry.get()
    team_B_name = team_B_entry.get()

    # Extract data for Team A and Team B
    team_A_data = df[df['Team'] == team_A_name][features]
    team_B_data = df[df['Team'] == team_B_name][features]

    # Make predictions for Team A and Team B using the pipeline
    team_A_prediction = pipeline.predict(team_A_data)[0]
    team_B_prediction = pipeline.predict(team_B_data)[0]

    # Convert numpy arrays to floats
    team_A_score = float(team_A_prediction)
    team_B_score = float(team_B_prediction)
    
    # Determine the winner
    if team_A_score > team_B_score:
        winner = f"{team_A_name} is predicted to win."
    elif team_B_score > team_A_score:
        winner = f"{team_B_name} is predicted to win."
    else:
        winner = "The game is predicted to be a tie."

    
