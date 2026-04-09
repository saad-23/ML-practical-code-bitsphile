import pandas as pd
import numpy as np


import pandas as pd


df = pd.read_csv("students.csv")

print(df)
# print(df.dropna())
# print(df["age"].dropna())
# print(df.dropna(subset=["age"]))

# df.loc[2,"city"] = np.nan

# print(df)

# print(df.fillna({
#     "age" : df["age"].mean(),
#     "city" : "unknown"
# }))
print(df.fillna({
    "age": df["age"].mean()
}))
print(df.loc[4,"age"].fillna("40"))




# Original Data
# data  = {
#     "name": ["ahmad","hamid",None],
#     "age" : [20,25,None],
#     "city": ["lahore","sargodha","karachi"]
# }

# df = pd.DataFrame(data)
# print("=== Original Data ===")
# print(df.info())
# print(df.isna())

# Add NULL/Missing Values
# print("\n=== Adding NULL Values ===")
# df.loc[1, "age"] = np.nan  # Add NULL to age
# df.loc[0, "city"] = None   # Add NULL to city
# print(df)

# # Check for NULL values
# print("\n=== Checking NULL Values ===")
# print(df.isnull())  # or df.isna()
# print("\nTotal NULL values per column:")
# print(df.isnull().sum())

# # Method 1: DROP rows with ANY NULL values
# print("\n=== Method 1: Drop Rows with NULL ===")
# df_dropped = df.dropna()
# print(df_dropped)

# # Method 2: DROP rows with NULL in SPECIFIC column
# print("\n=== Method 2: Drop Rows with NULL in 'age' ===")
# df_dropped_age = df.dropna(subset=['age'])
# print(df_dropped_age)

# # Method 3: FILL NULL values with a specific value
# print("\n=== Method 3: Fill NULL Values ===")
# df_filled = df.fillna({
#     "age": df["age"].mean(),  # Fill with average age
#     "city": "Unknown"         # Fill with 'Unknown'
# })
# print(df_filled)

# # Method 4: FILL NULL values with different strategies
# print("\n=== Method 4: Forward Fill (ffill) ===")
# df_ffill = df.fillna(method='ffill')
# print(df_ffill)

# # Method 5: DROP columns that have NULL values
# print("\n=== Method 5: Drop Columns with NULL ===")
# df_drop_cols = df.dropna(axis=1)
# print(df_drop_cols)