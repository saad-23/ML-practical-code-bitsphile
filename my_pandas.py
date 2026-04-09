import pandas as pd


df = pd.read_csv("students.csv")

print("**** original Data ***")
print(df)

print("**** Manipulated Data ***")

print(df.fillna({
    "fees": df["fees"].median(),
    "student_id" : "st-2026"
}))






# print(df.dropna())

# df.to_csv("newfile.csv",index=False)

# print(df.dropna(subset=["guardian_income"]))


# print(df["age"].max())
# print(df["age"].min())



# print(df.dropna())


# count null values for each column
# total_null_values = df.isna().sum()

# print(df["age"].isna().sum())



# print(total_null_values)




































# df.loc[df["age"] > 18 , "status"] = "adults"
# df.loc[df["age"] <= 18 , "status"] = "child"

# df.to_csv("result.csv",index=False)


