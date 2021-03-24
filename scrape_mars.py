#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



# In[2]:


#create path
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser



# In[3]:
def scrape():
    browser= init_browser()
    mars={}
    url= 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html= browser.html
    soup= bs(html, 'html.parser')
    results= soup.find('div', class_= 'list_text')
    title= results.find("a").text
    paragraph= results.find('div', class_= 'article_teaser_body').text
    mars["news_title"] = title
    mars["summary"] = paragraph
    url2= 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url2)
    html2= browser.html
    soup= bs(html2, 'html.parser')
    result= soup.find('div', class_= 'floating_text_area')
    link= result.find('a')['href']
    url_p= 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    url_f= url_p+link
    mars["JPL_url"] = url_f
    url3= 'https://space-facts.com/mars/'
    table= pd.read_html(url3)
    #slice dataframe
    df = table[0]
    #change columns type
    df.columns = df.columns.astype(str)
    #change index
    df_re= df.rename(columns={"0": "Description", "1": "Mars"})
    #set description as index
    df= df_re.set_index('Description')
    #convert data to html table
    mars_table= df.to_html()
    mars_table= mars_table.replace('\n', ' ')
    mars["table"] = mars_table
    #Cerberus Hemispheres
    hemi_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    hemis_img= []
    for i in range (4):
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        hemis_img.append(dictionary)
        browser.back()
    mars['mars_hemis'] = hemis_img
    browser.quit()   
    return mars





    








# In[ ]:







