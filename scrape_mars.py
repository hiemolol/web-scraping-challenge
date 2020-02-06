from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    main_dict = {}

    # Visit visitcostarica.herokuapp.com
    url = "https://visitcostarica.herokuapp.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

### NASA Mars News

url = "https://mars.nasa.gov/news/"
browser.visit(url)

html = browser.html
bsoup = BeautifulSoup(html, "html.parser")

main_dict["title"] = bsoup.find("article").find("div",class_='content_title').a.text
main_dict["paragraph"] = bsoup.find("article").find("div",class_='article_teaser_body').text

### Navigate site and find image url
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(featured_image_url)

html = browser.html
bsoup = BeautifulSoup(html, 'html.parser')

image_url = bsoup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

url = 'https://www.jpl.nasa.gov'
main_dict["featured_image"] = url + image_url

### Mars weather twitter
weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)

html = browser.html
bsoup = BeautifulSoup(html, 'html.parser')

tweet = soup.find_all('div', class_="js-tweet-text-container")
main_dict["weather"] = tweet[2]

### Mars facts
url = 'https://space-facts.com/mars/'
mars_facts = pd.read_html(url)

### Mars hemisphere
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemispheres_url)

html_hemispheres = browser.html
bsoup = BeautifulSoup(html_hemispheres, 'html.parser')


results = bsoup.find_all('div', class_='item')
main_dict["hemisphere_image_urls"] = []

#create loop
hemispheres_url = 'https://astrogeology.usgs.gov'
for result in results: 
    title = result.find('h3').text
    partial_url = result.find('a', class_='itemLink product-item')['href']
    browser.visit(hemispheres_url + partial_url)
    partial_html = browser.html
    bsoup = BeautifulSoup( partial_html, 'html.parser')
    img_url = hemispheres_url + bsoup.find('img', class_='wide-image')['src'] 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

#display urls    
main_dict["hemisphere_image_urls"]

return main_dict