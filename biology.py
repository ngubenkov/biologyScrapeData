from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import traceback

page_counter = 1

def first_open_url(url):
    #browser = webdriver.Chrome('/Users/frozmannik/PycharmProjects/biologyScrape/files/mac/chromedriver')  # fake Chrome browser mac
    browser = webdriver.Chrome('C:\\Users\Frozm\PycharmProjects\\biologyScrapeData\\files\win\chromedriver.exe')
    browser.get(url)
    accept_terms(browser) #uncoment this

    global page_counter
    f = open('links.txt', 'a')
    print('Page {}'.format(page_counter))
    f.write('Page {}'.format(page_counter) + '\n')
    f.close()
    page_counter = page_counter + 1

    get_items(browser)
    open_next_page(browser)

def accept_terms(browser):
    while True:
        try:
            accept_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-oe4so')))
            #myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
            print("Terms are accepted")
            accept_btn.click()
        except TimeoutException:
            print ("Cant accept terms")
            browser.refresh()
            continue
        break

def get_items(browser): # get links of all files
    while True:
        try:
          table = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
          lines = table.find_elements_by_tag_name("tr")
          for line in lines:
              if "FPKM" in line.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute("innerHTML"): # check name of file
                items_links.append(line.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute("href")) # add links
                f = open('links.txt', 'a')
                f.write(line.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute("href") + '\n')
                f.close()
        except TimeoutException:
            print("Cant get all items")
            browser.refresh()
            continue
        break


def open_next_page(browser):
    runner = True
    while runner:
        try:
            buttons = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'test-pagination-link')))
            for btn in buttons:
                if btn.find_element_by_tag_name("button").get_attribute("innerHTML") == '›':
                        global page_counter
                        print('Page {}'.format(page_counter))
                        page_counter = page_counter + 1
                        f = open('links.txt','a')
                        f.write('Page {}'.format(page_counter)+ '\n')
                        f.close()
                        open_url(browser,btn.get_attribute("href"))

        except TimeoutError:
            print("Cant go to next page")
            browser.refresh()
            continue
        finally:
            runner = False
            break
    print("last element")



def open_url(browser, url):
    browser.get(url)
    get_items(browser)
    open_next_page(browser)

if __name__ == '__main__':
    items_links = []
    url = 'https://portal.gdc.cancer.gov/repository?facetTab=files&files_size=100&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%5B%22TCGA-LUSC%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22files.data_category%22%2C%22value%22%3A%5B%22Transcriptome%20Profiling%22%5D%7D%7D%5D%7D&searchTableTab=files'
    #1url = "file:///Users/frozmannik/PycharmProjects/biologyScrape/files/Repository.htm"
    last_page = 'https://portal.gdc.cancer.gov/repository?facetTab=files&files_offset=2670&files_size=10&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%5B%22TCGA-LUSC%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22files.data_category%22%2C%22value%22%3A%5B%22Transcriptome%20Profiling%22%5D%7D%7D%5D%7D&searchTableTab=files'
    first_open_url(url)

    with open('lins_without_page.txt', 'w') as f:
        for item in items_links:
            f.write("{}\n".format(item))

    print("end of execution")