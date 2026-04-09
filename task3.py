
message = "anybody asks me to accept free invite for trial basis of any ai scheme application to use for any purpose"

spam_words = ["free","trial","scheme"]

for word in spam_words:
    if(word in message):
        message = message.replace(word,"****")


print(f"Total characters of new message: {len(message)} ")
print(message)

























#  below code is for find....
# names = ["faisal  ","  musa","hassan","darain"]
# scores = [60,45,30,78]
# status = ""
# for index, name in enumerate(names):
#     name = name.strip().upper()
#     if(scores[index] > 50):
#         status = "pass"
#     else:
#         status = "fail"

#     print(f"Rank {index+1} |  {name} | Score : {scores[index]} | status: {status}")




