import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import random
import datetime

# method for connecting and saving to the database
def store(title, price, image):
    sql = """INSERT INTO data_frame(title, price, image_url, created_at) VALUES(%s, %s, %s, %s);"""
    conn = None
    try:
        # connecting to the database
        conn = psycopg2.connect(dbname='sneakerdb', user='postgres', password = None)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (title, price, image, datetime.datetime.now())) 
        # commit the changes to the database
        cur.connection.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# url to scrape data
shoe_store_url = 'https://www.obeezi.com/sneakers?product_list_limit=120'

#Load html's plain data into a variable
plain_html_text = requests.get(shoe_store_url)

#parse the data
soup = BeautifulSoup(plain_html_text.text, 'lxml')
sneaker_container_divs = soup.find_all('div', class_='product-item-info', limit=5)

# Lists to store the scraped data in
sneakers_big_data = []

for sneaker_div in sneaker_container_divs:
    mini_tuple = tuple()
    mini_list = list(mini_tuple)

    # sneaker's name
    mini_list.insert(0, sneaker_div.strong.a.text.replace('\n', ''))
    # sneaker's price
    mini_list.insert(1, sneaker_div.find('span', class_='price').get_text())
    # sneaker's image_url
    mini_list.insert(2, sneaker_div.find('img', class_='product-image-photo')['src'])

    new_data = tuple(mini_list)
    sneakers_big_data.append(new_data)


for sneaker_data in sneakers_big_data:
    #store items into the database
    store(sneaker_data[0], sneaker_data[1], sneaker_data[2])


"""optional: store data in pandas data frame"""
# test_df = pd.DataFrame(
# {
#     'sneaker': sneaker_titles,
#     'image_url': sneaker_images,
#     'price': sneaker_prices,
# })
# print(test_df.info())
#test_df
