from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    slide_element = news_soup.select_one("ul.item_list li.slide")
    slide_element.find("div", class_="content_title")

    news_title = slide_element.find("div", class_="content_title").get_text()
    news_p = slide_element.find("div", class_="article_teaser_body").get_text()
    



#executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#browser = Browser("chrome", **executable_path, headless=False)

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    image_button = browser.find_by_id("full_image")
    image_button.click()

    browser.is_element_present_by_text("more info")
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    featured_img_url = image_soup.select_one("img").get("src")
    featured_img_url


    facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(facts_url)[1]


    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #browser = Browser("chrome", **executable_path, headless=False)
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    link = browser.find_by_css("a.product-item h3")
    for item in range(len(link)):
        hemisphere = {}
    
        browser.find_by_css("a.product-item h3")[item].click()
    
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
    
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
        hemisphere_image_urls.append(hemisphere)

    
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_img_url,
        "mars_facts": table,
        "hemispheres": hemisphere_image_urls}
     
    browser.quit()

    return mars_data