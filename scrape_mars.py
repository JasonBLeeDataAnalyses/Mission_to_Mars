# Dependencies
import pandas as pd
import re
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
import time

# Create function to execute scraping code
# Return Python dictionary containing scraped data
def scrape():
    # Use splinter with the chrome browser to scrape all the data
    executable_path = {'executable_path': '/usr/local.bin.chromedriver'}
    browser = Browser('chrome', headless=False)

    # Store all data (scraped)
    marsdata = {}

    # Scraping NASA Mars News
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(2)

    # Parsing w/ BS4
    news_soup = BeautifulSoup(browser.html, 'html.parser')

    # Retrieve the most recent news
    news_result = news_soup.find('div', class_='image_and_description_container')

    # Retrieve the latest news description
    description = news_result.find('div', class_='rollover_description_inner').text.strip()
    # print("News Description: " + description)

    # Retrieve the latest news title
    news_result = news_soup.find('div', class_='content_title')
    title = news_result.find('a').text.strip()
    # print("/nNews Title: " + title)

    # Append the title and description to marsdata
    marsdata['News'] = {"Title": title, "Description": description}

    # mars_parag = news_result.find_all('div', class_='rollover_description_inner')
    # time.sleep(2)
    # for article, paragraph in zip(news_titles, mars_parag):

    # # Make a dictionary to store article titles and paragraph texts
    #     mars = {}

    #     # Find article titles
    #     title = article.find('a')
    #     news_title = title.text
    #     mars['news_title'] = news_title

    #     # Find paragraph text
    #     p_text= paragraph.find('div')
    #     mars_p = p_text.text
    #     mars['news_p'] = mars_p
    #     #
    #     # if db.marsdata.find({<check title refer to docs>}).limit(1).size(
    #     print(mars)
    #     db.marsdata.insert(mars)

    # # Loop to get article titles and paragraph texts
    # for article in news_titles:

    #     # Make a dictionary to store article titles and paragraph texts
    #     mars_title_paragraph = {}

    #     # Find article titles
    #     title = article.find('a')
    #     news_title = title.text
    #     mars_title_paragraph['news_title'] = news_title

    #     scrape_mars_data.append(mars_title_paragraph)

    # for paragraph in mars_parag:

    #     # Make a dictionary to store article titles and paragraph texts
    #     mars_title_paragraph = {}

    #     # Find paragraph text
    #     p_text= paragraph.find('div')
    #     mars_p = p_text.text
    #     mars_title_paragraph['news_p'] = mars_p

    #     scrape_mars_data.append(mars_title_paragraph)

    # marsdata['news_data'] = scrape_mars_data

    # -------------------------------------
    # Obtain html of Mars space images website
    mars_img_browser = Browser('chrome', headless=False)
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_img_browser.visit(jpl_url)
    time.sleep(2)

    # Click button on top of featured image 'FULL IMAGE'
    mars_img_browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    # Click "more info"
    mars_img_browser.click_link_by_partial_text('more info')
    time.sleep(2)
    
    # Click on image link w/ fullsize img
    mars_img_links = mars_img_browser.find_link_by_partial_href('/spaceimages/images/largesize/')
    mars_img_links.first.click()
    time.sleep(2)

    # Parse html file with BeautifulSoup
    jpl_soup = BeautifulSoup(mars_img_browser.html, 'html.parser')
    # print(jpl_soup.prettify())

    featured_image_url = jpl_soup.find('img').get('src')
    # print("Featured Image URL: " + featured_image_url)

    marsdata['Featured_Image'] = featured_image_url

    # # Find image link with BeautifulSoup
    # mars_imgs = jpl_soup.find_all('div', class_='carousel_items')

    # # Loop through images
    # for img in mars_imgs:

    #     large_pic = img.find(class_='button fancybox').get('data-fancybox-href')
        
    #     featured_image_url = f'https://www.jpl.nasa.gov{large_pic}'

    #     # Append to featured image to main dictionary 'scrape_mars_data'
    #     marsdata['featured_image'] = featured_image_url

    # -------------------------------------
    # Create list to store dictionaries of weather info
    mars_weather_info = []

    # Get weather tweets with splinter
    twitter_browser = Browser('chrome', headless=False)
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_browser.visit(twitter_url)
    time.sleep(2)

    # Parse html file with BeautifulSoup
    twitter_html = twitter_browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')

    # Find weather tweets with BeautifulSoup
    weather_tweets = twitter_soup.find_all('p', class_='TweetTextSize')
    weather_tweets

    # Get tweets that begin with 'Sol' which indicate weather tweets
    weather_filter = 'Sol '

    for tweet in weather_tweets:
        if weather_filter in tweet.text and 'Happy' not in tweet.text:
            mars_weather = tweet.text

            # Create dictionary to gather all weather info from Mars weather twitter
            mars_weather_info_dict = {}

            # Add tweets to dictionary 'mars_weather_info_dict'
            mars_weather_info_dict['tweet_text'] = mars_weather

            # Append to weather tweets to main dictionary 'scrape_mars_data'
            mars_weather_info.append(mars_weather_info_dict)

    marsdata['tweets'] = mars_weather_info

    # -------------------------------------
    # Url to Mars facts website
    facts_url = 'https://space-facts.com/mars/'

    # Get table from url
    facts_table = pd.read_html(facts_url)

    # Select table
    mars_facts = facts_table[0]

    mars_facts = mars_facts.to_html()

    # Add facts to dictionary 'mars_facts_dict'
    marsdata['mars_facts'] = mars_facts.replace('\n', '')

    # -------------------------------------
    # Create list to store dictionaries of hemisphere title and image links
    hemispheres = []

    # Use splinter to get image and title links of each hemisphere
    usgs_browser = Browser('chrome', headless=False)
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    usgs_browser.visit(usgs_url)
    time.sleep(2)

    # Parse html file with BeautifulSoup
    hemi_soup = BeautifulSoup(usgs_browser.html, 'html.parser')

    # Find hemisphere image link and title
    hemi_items = hemi_soup.find_all('div', class_='item')

    # Loop through each link of hemispheres on page
    for item in hemi_items:
        title = item.find('h3').text.strip()

        # Retrieve full image title
        links = usgs_browser.find_link_by_partial_text(title)
        links.first.click()
        time.sleep(2)

        # Retrieve img url and append to main url
        soup = BeautifulSoup(usgs_browser.html, 'html.parser')
        found_hemi_url = soup.find('img', class_='wide-image').get('src')
        hemi_url = 'https://astrogeology.usgs.gov' + found_hemi_url

        links = usgs_browser.find_link_by_partial_text("Back")
        links.first.click()
        time.sleep(2)
        
        # Append dictionaries to list
        hemispheres.append({"title": title, "img_url": hemi_url})

        # Append to main dictionary 'scrape_mars_data'
    marsdata['hemispheres'] = hemispheres
    
    # print(marsdata)
    # print(marsdata)
    return marsdata

# scrape()

# # Create root/index to query MongoDB and pass data onto HTML template
# @app.route('/')
# def index():
#     marsdata = db.marsdata.find_one()
#     return render_template('index.html', marsdata=marsdata)

# @app.route('/scrape')
# def scrape():
#     data = scrape_mars()
#     # marsdata = db.marsdata.insert_many(data)
#     db.marsdata.update(
#         {},
#         data,
#         upsert=True
#     )
#     return "Scraping Successful!"