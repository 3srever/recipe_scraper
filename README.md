# recipes
A first shot at building a webscaper for recipes from the Marley Spoon website. 

The setup of files is as follows:

- **x_paths.py** - used to define all the xpath classes that scaper_main uses to find recipe content
- **scraper_class.py** - consists of 2 classes used for interacting with websites & grabbing content (spider & scraper respectively). both rely on selenium
- **marleyspoon.csv** - an example of the scraped data
- **chromedriver** - used by selenium to scrape in headless Chrome
- **scraper_main.py** - where the main logic happens in 3 steps:
1. in the first block, it grabs the available dates for recipes & let's the user pick a date to scrape. alternatively if the code is unchanged, it will just grab the last date available.
2. the second block will navigate to a domain (country), click the date of choice & grab the url of each recipes on that page
3. the third block navigates to each url, grabs the requested content & prepares it for use in a pandas dataframe.


### libraries required
- selenium
- selenium.webdriver.chrome.options
- pandas
- time
