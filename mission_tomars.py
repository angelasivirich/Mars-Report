from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
import requests
import time
import pandas as pd
from pandas.io.html import read_html
from pprint import pprint

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    ##NASA Mars News
    browser = init_browser()
    mars_info = {}

    nasa_url ='https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(10)
    soup = BeautifulSoup(browser.html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    mars_info['title'] = news_title
    mars_info['paragraph'] = news_p

    ## JPL Mars Space Images - Featured Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    time.sleep(10)
    soup = BeautifulSoup(html, "html.parser")
    browser.click_link_by_id('full_image')
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    browser.click_link_by_partial_href('/spaceimages/details.php?id')
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    browser_url = 'https://www.jpl.nasa.gov'
    image_url = soup.find('article').find('figure').find('a')['href']
    featured_image = browser_url + image_url
    mars_info['featured_image'] = featured_image

    ## Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_weather = soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[31].text
    mars_info['mars_weather'] = mars_weather

    ##Mars Facts
    facts_url ='https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Attribute', 'Value']
    mars_facts_df.set_index('Attribute', inplace=True)
    mars_facts_dic = mars_facts_df.to_dict() 
    mars_info['mars_facts'] = mars_facts_dic

    ## Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []
    hemisphere_list = ['Cerberus','Schiaparelli','Syrtis','Valles']
    for item in hemisphere_list:
        try:
            hemispheres = {}
            url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
            browser.visit(url)
            html = browser.html
            soup = BeautifulSoup(html,'html.parser')
            browser.click_link_by_partial_text(item)
            html = browser.html
            soup = BeautifulSoup(html,'html.parser')
            hemispheres['title'] = soup.find('h2',class_="title").text
            hemispheres['image'] = soup.find('ul').find('a')['href']
            mars_hemisphere.append(hemispheres)           
        except Exception as e:
            print(e)

    mars_info['mars_hemisphere'] = mars_hemisphere

    browser.quit()
    return mars_info




