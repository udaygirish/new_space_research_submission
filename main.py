import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from tqdm import tqdm
import re
import pandas as pd
import numpy as np
import argparse
import urllib3
from bs4 import BeautifulSoup
import csv
http=urllib3.PoolManager()
from utils import plotter as pt

def scroll_and_save(driver,html_filename):
    '''
    Function to scoll the website and save
    the page into a html format for futher processing
    Scroll number can be modified
    '''
    ScrollNumber = 5
    for i in tqdm(range(1,ScrollNumber)):
        driver.execute_script("window.scrollTo(1,50000)")
        time.sleep(5)

    file = open(html_filename, 'w')
    file.write(driver.page_source)
    file.close()
    driver.close()

def review_extract(input_val):
    '''
    Function to extract review from
    one of the html element
    '''
    temp_review = input_val.find_all('span',{'jsname':'bN97Pc'})
    temp_review = str(temp_review[0])
    temp_review = str(temp_review.split(">")[1].split("<")[0])
    return temp_review

def rating_extract(input_val):
    '''
    Function to extract rating from
    one of the html element
    '''
    temp_rating = input_val.find_all('div',{'class':'pf5lIe'})
    temp_rating = eval(str(temp_rating[0]).split('aria-label=')[-1].split("role")[0])
    temp_rating = int(re.findall('\d+',temp_rating)[0])
    return temp_rating

def html_read_and_get_data(html_filename):
    '''
    Function to read HTML and get required data
    and call different function to clean the data
    to get a proper rating and review data
    '''
    data = open(html_filename,'r')
    soup = BeautifulSoup(data, 'html.parser')   
    base_list = []
    for i in soup.find_all('div', {'jsname': 'fk8dgd'}):
        temp = i.find_all('div',{'jsmodel':'y8Aajc'})
        base_list.append(temp)
    total_rating = []
    total_review = []
    for i in base_list[0]:
        temp_review = review_extract(i)
        temp_rating = rating_extract(i)
        total_rating.append(temp_rating)
        total_review.append(temp_review)
    data = dict()
    data['Rating'] = total_rating
    data['Review'] = total_review
    return data
    
def save_csv(data,csv_path):
    '''
    Function to save the data (ratings 
    and reviews) as a CSV file
    '''
    df = pd.DataFrame(data, columns = ['Rating', 'Review']) 
    df.to_csv(csv_path)
    return df

def main():
    '''
    Main function
    Arguments:
    -url : url which needs to be scraped
    -fn : filepath for maintaing organized outputs
    default is set to test
    '''

    parser = argparse.ArgumentParser()  
    parser.add_argument("-url", "--web_url", required=True, help = "URL PATH for which u need wordcloud") 
    parser.add_argument("-fn", "--filepath", required=False,default='test', help = "URL PATH for which u need wordcloud") 
    args = parser.parse_args()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])

    driver.get(str(args.web_url))
    web_review_url = str(args.web_url)+"&showAllReviews=true"
    driver.get(web_review_url)
    html_filename = "output/"+str(args.filepath)+".html"
    scroll_and_save(driver,html_filename)
    data= html_read_and_get_data(html_filename)
    
    csv_path = "output/"+str(args.filepath)+".csv"
    df = save_csv(data,csv_path)

    rating_1_df = df[df['Rating']==1]
    rating_1_reviews = np.asarray(df['Review']).tolist()

    rating_5_df = df[df['Rating']==5]
    rating_5_reviews = np.asarray(df['Review']).tolist()

    rating_1_img_path = "output/"+str(args.filepath)+"_rating_1.png"
    rating_5_img_path = "output/"+str(args.filepath)+"_rating_5.png"

    pt.wordcloud_generator(rating_1_reviews,rating_1_img_path)
    pt.wordcloud_generator(rating_5_reviews,rating_5_img_path)


if __name__ == "__main__":
    main()