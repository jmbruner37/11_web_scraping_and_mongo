from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt
import time
import requests as req

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    slide_element = news_soup.select_one("ul.item_list li.slide")
    slide_element.find("div", class_="content_title")

    news_title = slide_element.find("div", class_="content_title").get_text()
    news_p = slide_element.find("div", class_="article_teaser_body").get_text()
    
    time.sleep(3)

#executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#browser = Browser("chrome", **executable_path, headless=False)

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(3)
    image_button = browser.find_by_id("full_image")
    image_button.click()

    browser.is_element_present_by_text("more info")
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    featured_img_url = image_soup.select_one("img").get("src")
    


    url="https://space-facts.com/mars/"

    #scrape table with pandas
    tables = pd.read_html(url)
    mars_df = tables[0]
    #set index
    mars_df.columns = ['Attribute', 'Value']
    clean_mars_df = mars_df.set_index('Attribute', inplace=True)

    #convert to html
    clean_mars_table = mars_df.to_html()
    


    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #browser = Browser("chrome", **executable_path, headless=False)
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(3)
    html = browser.html 
    h_soup = BeautifulSoup(html,"html.parser") 
    results = h_soup.find_all("div",class_='item')
    hemisphere_image_urls = []

    for result in results:
        product_dict = {}
        titles = result.find('h3').text
        end_link = result.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup= BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        product_dict['title']= titles
        product_dict['image_url']= image_url
        hemisphere_image_urls.append(product_dict)
    
    
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_table": clean_mars_table,
        "featured_image": featured_img_url,
        "hemispheres": hemisphere_image_urls}
     
    browser.quit()
    print(mars_data)
    return mars_data