# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # # Parsing News Titles from 'https://redplanetscience.com' page

    url = 'https://redplanetscience.com'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # Examine the results, then determine element that contains sought info
    cont_title = soup.body.find_all('div', class_="content_title")
    cont_title

    cont_para = soup.body.find_all('div', class_="article_teaser_body")
    cont_para

    # Loop through returned results

    for title, para in zip(cont_title, cont_para):
        # Error handling
        try:
            # Identify and return title of listing
            new_title = title.text
            new_para = para.text


            # Print results only if title
            if (title):
                print('-------------')
                print(f'Article title:  {new_title}')
                print(f'Paragpraph: {new_para}', '\n')
        except AttributeError as e:
            print(e)


    # # Saving featured image 

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    featured_image = soup.body.find('a', class_="showimg fancybox-thumbs")['href']
    featured_image
    featured_image_url = url + featured_image
    print(f'featured_image_url= {featured_image_url}')


    # # Mars Facts
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    url = 'https://galaxyfacts-mars.com/'
    profile_table = pd.read_html(url)
    #profile_table

    #check numebr of tables parsed
    #len(profile_table)

    df = profile_table[0]
    #df.head(10)

    df.columns = df.iloc[0]
    mars_df = df[1:]
    mars_df = mars_df.reset_index(drop=True)
    mars_df = mars_df.rename(columns={"Mars - Earth Comparison": "Parameter"})
    mars_df = mars_df[["Parameter","Mars", "Earth"]]
    mars_df



    # Use Pandas to convert the data to a HTML table string.
    #convert the data to a HTML table string
    mars_html_table = mars_df.to_html(classes='table table-striped', index = False)
    #mars_html_table = mars_html_table.replace('\n', '')
    mars_html_table

    # # Mars Hemispheres

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # Examine the results, then determine element that contains sought info
    hemisphere = soup.body.find_all('div', class_="description")
    hemisphere

    # Loop through main web page to get links for each hemisphere pages
    hemisphere_links = []
    for hemlink in hemisphere:

        # Error handling
        try:
            link = hemlink.a["href"]   
            if (link):
                   hemisphere_links.append(url+link)
        except AttributeError as e:
            print(e)
    #hemisphere_links

    #loop through each hemisphere pages to get images and titles and save it to the list as dictionaries

    hemisphere_list = []

    for singlelink in hemisphere_links:
        hem_url = singlelink
        browser.visit(hem_url)
        soup = BeautifulSoup(browser.html, 'html.parser')
        image_url = soup.body.find('img', class_="wide-image")["src"]
        hem_title = soup.body.find('h2', class_="title").text
        #print(hem_title)
        #print(url+image_url)
        #print("-----------")
        hemisphere_list.append({"Title": hem_title, "Image ULR":url+image_url})
    hemisphere_list
    
    #store all values in a dictionary
    mars_dictionary = {
        "title": new_title,
        "Paragrapth": new_para,
        "Featured_image": featured_image_url,
        "Mars_facts": mars_html_table,
        "Hemisphiers":hemisphere_list 
    }
    
    browser.quit()

    return mars_dictionary




