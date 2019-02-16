from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from sys import path

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):  # check if response is coree
    content_type = resp.headers['Content-type'].lower()
    return(resp.status_code == 200
           and content_type is not None
           and content_type.find('html') > -1)

def open_url(url):
    browser = webdriver.Chrome('/Users/frozmannik/PycharmProjects/biologyScrape/files/chromedriver')  # fake Chrome browser
    browser.get(url)
    #accept_terms(browser) #uncoment this
    get_items(browser)
    open_next_page(browser)


def accept_terms(browser):
    delay = 10
    try:
        accept_btn = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-oe4so')))
        #myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
        print("Page is ready!")
        accept_btn.click()
    except TimeoutException:
        print ("Loading took too much time!")


def get_items(browser): # get links of all files
    delay = 10
    try:
      table = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
      lines = table.find_elements_by_tag_name("tr")
      for line in lines:
          if "FPKM" in line.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute("innerHTML"): # check name of file
            items_links.append(line.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute("href")) # add links
            # print(line.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute("innerHTML")) # name of file
            #print(line.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute("href"))  # link of file
    except TimeoutException:
       print("Loading took too much time!")


def open_next_page(browser):
    buttons = WebDriverWait(browser, 0).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'test-pagination-link')))
    for btn in buttons:
        if btn.find_element_by_tag_name("button").get_attribute("innerHTML") == '›':
            print('Button Found')
        else:
            print("Not this button: {}".format(btn.find_element_by_tag_name("button").get_attribute("innerHTML")))


if __name__ == '__main__':
    items_links = []
    #url = 'https://portal.gdc.cancer.gov/repository?facetTab=files&files_size=10&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%5B%22TCGA-LUSC%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22files.data_category%22%2C%22value%22%3A%5B%22Transcriptome%20Profiling%22%5D%7D%7D%5D%7D&searchTableTab=files'
    url = "file:///Users/frozmannik/PycharmProjects/biologyScrape/files/Repository.htm"
    open_url(url)
    print(items_links)