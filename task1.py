students = ["  ali  ", "sara", "  hassan", "zoya  "]
marks = [45, 82, 30, 95]

for i, name in enumerate(students):
    clean_name = name.strip().upper()
    score = marks[i]
    
    status = "PASS" if score >= 50 else "FAIL"
    
    print(f"Rank {i+1}: {clean_name} | Score: {score} | Status: {status}")




# age = input("Enter age:")

# if(age > 25):
#     print("yes correct")
# else:
#     print(f"wrong")
