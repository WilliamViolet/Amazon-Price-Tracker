###############################################################################
#
# Version 1.0.0
#
###############################################################################
import requests 
from bs4 import BeautifulSoup
import smtplib #simple mail ptotocol

#global variable to define the header for our crawler
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

###############################################################################
# Description: function reads input file and formats to dictionary 
#              key being link and data being price wall
# 
# Inputs: None
#
# Outputs: Dictionary {Link, price threshold}
#
# Issues: None
def read_file():
    file = open("items_to_track.txt", "r")
    data = file.read()
    data_list = data.splitlines()
    data_dic = {}
    for item in data_list:
        temp = item.split(',')
        data_dic[temp[0]] = temp[1]

    #print(data_dic)
    return data_dic
###############################################################################

###############################################################################
# Description:
#
# Inputs: 
#
# Outputs: 
#
# Issues: 
def check_price(url_dic):
    item_data = {}
    for key in url_dic:
        #creating the soup
        page = requests.get(key, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        #grabbing title of item from soup
        title = soup.find(id="productTitle").get_text().strip()
      
        #grabbing price of item from soup
        priceString = soup.find(id="priceblock_ourprice").get_text()
        price = float(priceString[1:7])

        #comparing price to target price
        if price <= float(url_dic[key]):
            item_data[title] = key

    send_mail(item_data)
###############################################################################
#Description: This emails my personal email from the bot email
#
#Email for scraper:            princetrackingbot@gmail.com 
#                              Username: pricetrackingbot
#                              Password: Pr1cetr@ck1ng6o7
#
# personal email app password: vjqnbadbcjbnyasb
#
# bot email password:          ubvzlofljjoqjxmr
#
# input: dictionary of title and link of the item that dropped price
#
# output: none
#
# sends: message to server to email data
#
# Error: No Items Error
def send_mail(item_data):
    if bool(item_data):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('pricetrackingbot@gmail.com', 'ubvzlofljjoqjxmr')

        subject_list = []
        link_list = []
        for item in item_data:
            subject_list.append(item)
            link_list.append(item_data[item])       

        i = 0
        subject = 'Prices Fell!'
        body = ""
        for link in link_list:
            body += subject_list[i] + ": " + link + "\n\n"
            i+=1

        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail(
            'pricetrackingbot@gmail.com',
            'willmviolet@gmail.com',
            msg
            )

        print('Email sent successfully')
        server.quit()

    else:
        print("No prices have fallen")
###############################################################################

url_dic = read_file()
check_price(url_dic)








