from bs4 import BeautifulSoup 
import requests

page_html=requests.get("http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=GTX&bop=And&Page=1&PageSize=36&order=BESTMATCH").text
page_soup=BeautifulSoup(page_html,'lxml')
cards = page_soup.find_all("div", {"class": "item-container"})

for card in cards: 
    priority = card.div.select("a")
    brand = priority[0].img["title"].title()
    product_name = card.div.select("a")[2].text
    shipping = card.find_all("li", {"class": "price-ship"})[0].text.strip().replace("$", "").replace(" Shipping", "")
    print("brand: " + brand + "\n")
    print("product_name: " + product_name + "\n")
    print("shipping: " + shipping + "\n")

     

