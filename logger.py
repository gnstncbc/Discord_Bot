# logger.py

import pandas as pd
import datetime

# Define a global DataFrame to store log entries
df_logs = pd.DataFrame(columns=['Product', 'Brand', 'Price', 'Datetime'])

async def log_data(data, channel):
    global df_logs  # Declare the DataFrame as global to access and modify it within the function
    
    formatted_local_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add the formatted_local_datetime column to the data DataFrame
    data['Datetime'] = formatted_local_datetime

    # Append the new data to the global DataFrame
    df_logs = df_logs.append(data, ignore_index=True)

async def return_logs():
    return df_logs