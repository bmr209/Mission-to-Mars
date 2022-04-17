# Import Splinter, BeautifulSoup, and Pandas
from dataclasses import dataclass
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    
    # Intiate headless driver for deployment
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_data(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# Upadate script to use functions to allow for easy reuse
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')

        # Begin scraping 
        # chaining .find to slide_elem says "This variable holds a ton of info, so look inside to find this specific data."
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ### JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #img_url

    return img_url


# ## Mars Facts
def mars_facts():
    
    #Add try/except for error handling
    try:

        # Scrape the entire table from anothe webpage with Pandas' .read_html() function
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    df

    # To convert the DF back into HTML-ready code to put in our new webpage, add bootstrap
    return df.to_html(classes="table table_striped")


# Scraping the hemisphere data
def hemisphere_data(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    links = browser.find_by_css('a.product-item img')

    for x in links:
        print(x)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        hemisphere = {}
        
        browser.find_by_css('a.product-item img')[i].click()
        
        html = browser.html
        html_soup = soup(html, 'html.parser')
        
    #   links = html_soup.find('a').get('href')
        links = html_soup.find('a')['href']
        
        titles = html_soup.find('h2', class_='title').get_text()
        
        samples = browser.links.find_by_text('Sample').first

        hemisphere['img_url'] = samples['href']
        hemisphere['title'] = titles
        
        hemisphere_image_urls.append(hemisphere)
        
        browser.back()

    print(hemisphere_image_urls)

    return hemisphere_image_urls
    
#browser.quit()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

