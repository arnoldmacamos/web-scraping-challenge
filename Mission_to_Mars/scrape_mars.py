from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(nasa_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    mars_news = soup.select(".item_list .slide")
    news_title = ''
    news_p = ''
    for nitem in mars_news:
        news_title =  nitem.select_one(".content_title a").text
        news_p = nitem.select_one(".article_teaser_body").text
        break
    #print(f"news_title = {news_title}")
    #print(f"news_p = {news_p}")

    #JPL Mars Space Images - Featured Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")    

    jpl_news = soup.select(".articles .slide")
    featured_image_url = ''
    for nitem in jpl_news:
        featured_image_url  =  'https://www.jpl.nasa.gov' + nitem.select_one(".fancybox")["data-fancybox-href"]
        break    
    #print(f"featured_image_url = {featured_image_url}")


    # Twitter Mars News
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")    

    tweets =  soup.select("div[class='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'] span")
    mars_weather = ''
    for tweet in tweets:
        if tweet.text.startswith('InSight sol'):
            mars_weather = tweet.text
            break
    #print(f"mars_weather = {mars_weather}")

    # Mars Facts
    space_url = "https://space-facts.com/mars"
    browser.visit(space_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")    

    fact_cols = soup.select("#tablepress-p-mars tr")

    descriptions = []
    values = []
    for col in fact_cols:
        descriptions.append(col.select_one(".column-1 strong").text)
        values.append(col.select_one(".column-2").text)

    dict_facts = {"Description": descriptions, "Value": values}
    df_facts=pd.DataFrame(dict_facts)
    mars_facts = df_facts.to_html()
    #print(f"mars_facts = {mars_facts}")


    # Mars Hemispheres
    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")    

    items = soup.select(".item")
    hemisphere_image_urls = []

    for item in items:
        title = item.select_one(".description h3").text
        img_href =  item.select_one("a")["href"]
 
        browser.visit(f"https://astrogeology.usgs.gov{img_href}" )
        time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")
        
        fimg_href = soup.select_one(f".downloads a")["href"]        
        hemisphere_img = {"title":title, "img_url":fimg_href}        
        hemisphere_image_urls.append(hemisphere_img)

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_weather": mars_weather,
        "featured_image_url":featured_image_url,
        "mars_facts":mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }  
              
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
