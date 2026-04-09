products_details  = {
    "product1" : {"title" : "laptop","price" : 50000, "quantity" : 10},
    "product2" : {"title" : "mobile","price" : 30000, "quantity" : 20},
    "product3" : {"title" : "earbuds","price" : 2000, "quantity" : 100},
    "product4" : {"title" : "tablets","price" : 45000, "quantity" : 5},
    "product5" : {"title" : "mouse","price" : 500, "quantity" : 500},
}

total = 0
for product_number , prod_detail in products_details.items():
    total = total + prod_detail["price"]


print(total)






# student = {
#     "student_id" : "bss23023",
#     "name" : "rizwan",
#     "age" : 25
# }

# for key, value in student.items():
#     print(value)

















# student = {
#     "name" : "adnan",
#     "age" : 26,
#     "gender" : "male",
#     "marks" : [50, 60,70,89]
# }

# print(student["marks"][2])