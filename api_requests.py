import requests


data = {
    "name" : "ahmad",
    "age" : 30
}

response = requests.post("https://jsonplaceholder.typicode.com/posts",json=data)


print(response)

