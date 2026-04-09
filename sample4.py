import requests

url = "https://jsonplaceholder.typicode.com/posts"
payload = {
    "title": "Hello World",
    "body": "This is an API call from Python!",
    "userId": 1
}
response = requests.post(url,json=payload)

# Sending the data as JSON
response = requests.post(url, json=payload)


print(f"Status Code: {response.status_code}")
print(f"Server Response: {response.json()}")









# def replaceSpamWords():
#     message = "anybody asks me to accept free invite for trial basis of any ai scheme application to use for any purpose"


#     spam_words = ["free","trial","scheme"]
#     for word in spam_words:
#         if(word in message):
#             message = message.replace(word,"****")


#     print(f"Total characters of new message: {len(message)} ")
#     print(message)


# replaceSpamWords()