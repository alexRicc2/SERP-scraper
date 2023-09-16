from googlesearch import search

query = input("enter your query: ")

for i in search(query, num_results=10, lang="en"):
  print(i)