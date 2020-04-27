# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class Spider():

    def __init__(self, path, delay=1):
        #run firefox webdriver from executable path of your choice
        #path = r"C:\Users\stefa\PycharmProjects\RecipeScraper\chromedriver\chromedriver.exe"
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.path = path
        self.delay = delay
        self.driver = webdriver.Chrome(
            executable_path=f"{self.path}",
            options = self.chrome_options
        )

    def get_url(self, url):
        #get web page from which to scrape, wait 5 seconds for it to load
        self.driver.get(url)
        time.sleep(self.delay)

    def quit(self):
        self.driver.quit()

    def scroll_down(self):
        #scroll to bottom of the page to initialise all scripts
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);\
            var lenOfPage=document.body.scrollHeight;\
            return lenOfPage;"
        )
        time.sleep(self.delay)

    def click(self, web_element):
        web_element.click()
        time.sleep(self.delay)

class Scraper(Spider):

    def __len__(self, web_element_list):
        # returns number of elements in a given list of webelements
        return len(self.show_text(web_element_list))

    def grab_web_element(self, goal_class):
        return self.driver.find_elements_by_xpath(
            goal_class
        )

    def grab_web_element_list(self, list_class, index_class, element_class):
        #point at a class that holds multiple subclasses (list_class)
        #define the direct child of that list class without the index (index_class)
        #and the element you want to scrape from each child (element_class)

        num_items = self.__len__(
            self.grab_web_element(
                list_class + index_class
            )
        )

        web_element_list = []
        for num in range(1, num_items + 1):
            element = self.grab_web_element(
                list_class + index_class + f'[{num}]' + element_class
            )
            web_element_list.append(element[0])
        return web_element_list

    def grab_index(self, goal_class, choice=3):
        #waits one second after to avoid overloading traffic
        #takes a clickable xpath (indicated by an index)
        index_choice = goal_class + f'[{choice}]'
        index_path = self.grab_web_element(
            index_choice
        )[0]
        return index_path

    def show_text(self, web_element_list):
        #checks if list consists of nested lists
        #then returns the text from webelements or list of webelements
        if isinstance(web_element_list[0], list):
            nested_list = []
            for subelem in web_element_list:
                nested_list.append([elem.text for elem in subelem])
            return nested_list
        else:
            return [elem.text for elem in web_element_list]

    def show_href(self, web_element_list):
        if isinstance(web_element_list[0], list):
            nested_list = []
            for subelem in web_element_list:
                nested_list.append([elem.get_attribute('href') for elem in subelem])
            return nested_list
        else:
            return [elem.get_attribute('href') for elem in web_element_list]