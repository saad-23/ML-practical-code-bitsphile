def validateUsername(username):
    if(username and username.isalpha()):
        return True
    else:
        return False
    



def validatePassword(password):
    has_letter = False
    has_digit = False
    for char in password:
        if char.isalpha():
            has_letter = True
        elif char.isdigit():
            has_digit = True

    if has_letter and has_digit:
        print("The string contains both letters and digits.")
    else:
        print("The string does not meet both criteria.")


validatePassword("test")










    

# def validatePassword(password):
#     results = []
#     if(password.isdigit()):
#         results.append(True)
#     if(password.isalpha()):
#         results.append(True)
#     return results



# password = input("enter password:")

# password_result = validatePassword(password)

# print(password_result)




# username =  input("Enter username:")
# result = validateUsername(username)
# if(result):
#     print("username ia valid")
# else:
#     print("username is not valid")
