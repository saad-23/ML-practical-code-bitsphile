import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# STEP 1: Data Preprocessing (Cleaning)
# ---------------------------------------------------------

# CSV Load krna
df = pd.read_csv('students.csv')
print("--- Original Data ---")
print(df.head())

# 1. Duplicates check krna aur remove krna
# PURPOSE: Agar aik hi student ka record do baar aa jaye to visualization galat ho sakti hai.
df = df.drop_duplicates()

# 2. Missing Values (NaN) handle krna
# PURPOSE: Agar data missing ho to ML model training me error de sakta hai.
# Age missing hai to mean (average) se fill kr denge
df['age'] = df['age'].fillna(df['age'].mean())
# Fees missing hai to median se fill kr denge
df['fees'] = df['fees'].fillna(df['fees'].median())
# Attendance missing hai to 0 se fill krte hain ya drop krte hain
df['attendance_percent'] = df['attendance_percent'].fillna(0)

# 3. String/Text cleaning
# NAME me extra spaces handle krna
df['Name'] = df['Name'].str.strip()
# City me lowercase/extra spaces handle krna
df['city'] = df['city'].str.strip().str.capitalize()

print("\n--- Cleaned Data (Glimpse) ---")
print(df.head())

# ---------------------------------------------------------
# STEP 2: NumPy Usage (Easy Way)
# ---------------------------------------------------------
# NumPy mathematics aur array manipulation ke liye best hai.

# DF column ko array me convert krna
gpa_array = df['gpa'].values 

print("\n--- NumPy Examples ---")
print(f"Total Students (using NumPy): {np.size(gpa_array)}")
print(f"Average GPA: {np.mean(gpa_array):.2f}")
print(f"Highest GPA: {np.max(gpa_array)}")

# Masking: Check krna kitne students ka GPA 3 se upar hai
toppers = gpa_array[gpa_array > 3.0]
print(f"Toppers Count: {len(toppers)}")

# ---------------------------------------------------------
# STEP 3: Outliers Detection & Solution
# ---------------------------------------------------------
# OUTLIERS: Wo values jo baqi data se bilkul alag (bohat barri ya bohat choti) hon.
# Example: Hamare data me 'age' 200 hai jo ke galat hai.

# Visualizing Outliers using Boxplot
plt.figure(figsize=(8, 4))
plt.boxplot(df['age'], vert=False)
plt.title('Age Outlier Check')
plt.show()

# SOLUTION for Outliers: 
# Hum filter apply krte hain (z-score ya manual limits)
# Let's say, valid age 15 se 50 ke beech honi chahiye
df = df[(df['age'] > 15) & (df['age'] < 50)]

# Attendance 100% se zyada nahi ho sakti, usay bhi fix krte hain (ST-1006 ka 102 hai)
df.loc[df['attendance_percent'] > 100, 'attendance_percent'] = 100

# Fees negative nahi ho sakti, usay absolute value bana dete hain (ST-1010)
df['fees'] = df['fees'].abs()

print("\n--- After Outlier Removal ---")
print(df[['Name', 'age', 'attendance_percent', 'fees']].head(10))

# ---------------------------------------------------------
# STEP 4: Matplotlib Visualizations
# ---------------------------------------------------------

# 1. Histogram: Age distribution dekhne ke liye
plt.figure(figsize=(6, 4))
plt.hist(df['age'], bins=5, color='skyblue', edgecolor='black')
plt.xlabel('Age')
plt.ylabel('No. of Students')
plt.title('Student Age Distribution')
plt.show()

# 2. Scatter Plot: Attendance vs GPA ka taluq (Relationship)
plt.figure(figsize=(6, 4))
plt.scatter(df['attendance_percent'], df['gpa'], color='green')
plt.xlabel('Attendance %')
plt.ylabel('GPA')
plt.title('Attendance vs GPA Correlation')
plt.show()

# ---------------------------------------------------------
# Stepwise Guide For Students (ML Path)
# ---------------------------------------------------------
# 1. Data Collection: Rozana ki buniyaad pe CSV/Database se data jama krna.
# 2. Preprocessing: Ganda data (Nulls, Duplicates, Outliers) saaf krna. (Yehi humne upar kiya)
# 3. EDA (Exploratory Data Analysis): Graphs bana kr patterns samjhna (Matplotlib/Seaborn).
# 4. Feature Engineering: Model ke liye zaruri columns chun-na (e.g. Attendance predict krne ke liye Fees zaruri nahi shayad).
# 5. Model Training: Scikit-Learn library use kr ke "train_test_split" krna.
# 6. Evaluation: Check krna model kitna accurate hai.
