import pandas as pd

# 1. Excel file load karein
df = pd.read_excel('updated_data.xlsx')




# 2. Logic: Jahan Name 'Afshan Nawaz' ho AUR User ID 299 ho, wahan User ID badal dein
# Maan lein nayi ID 500 hai
nayi_id = 14
df.loc[(df['Name'] == 'Mohsin Raza') & (df['User ID'] == 193), 'User ID'] = nayi_id

# 3. File wapas save karein
try:
    df.to_excel('updated_data.xlsx', index=False)
    print("Data successfully 'User ID' column mein update ho gaya hai!")
except PermissionError:
    print("Error: 'updated_data.xlsx' file shayad Excel mein open hai. Usse band karke dobara run karein.")
except Exception as e:
    print(f"Ek error aaya hai: {e}")