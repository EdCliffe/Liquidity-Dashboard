"""The Scraper class is the base class which contains useful methods for
webscraping.

    Main Features:
    -------------
        - Using BeautifulSoup
            - Create a BeautifulSoup object from a given URL
            - Find web-links from a data-table BeautifulSoup object
        - Using Selenium
            - Request a Url
            - Send keys to an html element id
            - Click an element using xpath
            - Click an element using id
            - Gather links from a table
            - Download images
            - Save data to a file
            """
# %%
import time
from selenium import webdriver
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self) -> None:
        self.url = None
        self.soup = None
        self.driver = webdriver.Chrome
        self.link_list = []
        pass



    def sel_get_url(self, url: str):

        """Use selenium to navigate to a chosen url.

        Keyword arguments:
        -----------------
        driver - the selenium webdriver of choice
        url - desired url as string
        """

        driver = self.driver
        driver.get(url)
        time.sleep(4)

    def sel_send_keys_id(self, element_id: str, keys: str):

        """Use selenium to send keys to a chosen element on the page.

        Keyword arguments:
        -----------------
        driver - the selenium webdriver of choice
        element_id - the id of the element to send keys to, string
        keys - characters to send to the page element, string
        """
        
        driver = self.driver
        driver.find_element(By.ID, element_id).send_keys(keys)

    def sel_click_xpath(self, xpath: str):

        """Use selenium to click an element, identified by xpath.

        Keyword arguments:
        -----------------
        driver - the selenium webdriver of choice
        xpath - the xpath address of the element to click
        """

        driver = self.driver
        try:
            driver.find_element(By.XPATH, xpath).click()
        except NoSuchElementException:
            return None

    def sel_click_id(self, id: str):

        """Use selenium to click an element, identified by id.

        Keyword arguments:
        -----------------
        driver - the selenium webdriver of choice
        id - the id of the element to click
        """

        driver = self.driver
        driver.find_element(By.ID, id).click()


    def sel_links_from_table(self, table_class_name: str,
                             element_class_name: str,
                             link_attribute: str) -> list:
        """Use selenium to retrieve links stored in a table.
        Nested 3 layers deep from the page -> table -> element -> link

        Keyword arguments:
        -----------------
        driver -- the selenium webdriver of choice
        table_class_name -- string identifying the data table
        element_class_name -- string identifying the class of the element
        link_attribute -- string identifying the attribute of the link in
                          the element

        Returns:
        -------
        list of links
        """

        driver = self.driver
        link_table = driver.find_element(By.CLASS_NAME, table_class_name)

        link_list = link_table.find_elements(By.CLASS_NAME, element_class_name)

        temp_link_list = []

        for item in link_list:
            # link = item.find_element_by_tag_name('a')
            temp_link_list.append(item.get_attribute(link_attribute))

        self.link_list.append(temp_link_list)
        return self.link_list



    def save_results(self, data, filename: str) -> json:

        """ Saves results objects to JSON format.

        Keyword arguments:
        ------------------
        data - a resulting data object, list, dictionary etc
        filename -  desired name of file,
                    which in this case includes the desired directory path
        """

        with open(filename, mode='w') as f:
            json.dump(data, f)

        return

    if __name__ == "__main__":
        print('done!')
        pass
