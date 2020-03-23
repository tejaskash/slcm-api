from bs4 import BeautifulSoup
html  ""
with open("temp.html","r") as f:
    html = f.read()

soup = BeautifulSoup(html,"html.parser")
maindiv = soup.find("div",{"id":"accordion1"})
print(maindiv)