import requests
import pyperclip
import sys

problem = sys.argv[1]

if(problem == "tsp"):
    url = "https://raw.githubusercontent.com/Pranavkak/cheaters/main/tsp.txt"
elif(problem == "2jug"):
    url = "https://raw.githubusercontent.com/Pranavkak/cheaters/main/2jug.txt"
elif(problem == "cost"):
    url = "https://raw.githubusercontent.com/Pranavkak/cheaters/main/cost.txt"
elif(problem == "bfs"):
    url = "https://raw.githubusercontent.com/Pranavkak/cheaters/main/bfs.txt"
elif(problem == "dfs"):
    url = "https://raw.githubusercontent.com/Pranavkak/cheaters/main/dfs.txt"
elif(problem == "bbfs"):
    url = "https://raw.githubusercontent.com/Pranavkak/cheaters/main/bbfs.txt"
elif(problem == "bdfs"):
    url = "https://raw.githubusercontent.com/Pranavkak/cheaters/main/bdfs.txt"
elif(problem == "8"):
    url = "https://raw.githubusercontent.com/Pranavkak/cheaters/main/8.txt"

response = requests.get(url)
content = response.content.decode()  # decode the bytes into a string

pyperclip.copy(content)

