from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import threading
import os
import tarfile
import gzip
import time

page_counter = 1

def browser_setup():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "/Users/frozmannik/Desktop/LUAD data"}
    chromeOptions.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(executable_path = '/Users/frozmannik/PycharmProjects/biologyScrape/files/mac/chromedriver',
                               chrome_options = chromeOptions)  # fake Chrome browser mac
    # browser = webdriver.Chrome('C:\\Users\Frozm\PycharmProjects\\biologyScrapeData\\files\win\chromedriver.exe')
    return browser

def first_open_url(url):
    browser = browser_setup()
    browser.get(url)
    accept_terms(browser) #uncoment this

    # save activity in file
    global page_counter
    f = open('links.txt', 'a')
    print('Page {}'.format(page_counter))
    f.write('Page {}'.format(page_counter) + '\n')
    f.close()

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

                f = open('links_without_page.txt', 'a')
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
                        page_counter = page_counter + 1
                        print('Page {}'.format(page_counter))
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

def file_to_list(file):
    with open(file, "r") as fd:
        lines = fd.read().splitlines()
    return lines

def download_from_links(links,firstInd, thread=1):
    browser = browser_setup()
    terms = True
    for num, link in enumerate(links, start=firstInd):
        browser.get(link)
        if terms: # accept terms first time
            try:
                accept_terms(browser)
                terms = False
            except:
                pass
        try:
            download_btn = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'test-download-button')))
            download_btn.click()

        except TimeoutException:
            try:
                print("Thread {}. TimeoutException 1 for file {} ".format(thread, num))
                browser.refresh()
                download_btn = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'test-download-button')))
                download_btn.click()
            except TimeoutException:
                try:
                    print("Thread {}. TimeoutException 2 for file {} ".format(thread, num))
                    browser.refresh()
                    download_btn = WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'test-download-button')))
                    download_btn.click()
                except TimeoutException:
                    try:
                        print("Thread {}. TimeoutException 3 for file {} ".format(thread, num))
                        browser.refresh()
                        download_btn = WebDriverWait(browser, 40).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'test-download-button')))
                        download_btn.click()
                    except TimeoutException:
                        try:
                            print("Thread {}. TimeoutException 4 for file {} ".format(thread, num))
                            browser.refresh()
                            download_btn = WebDriverWait(browser, 40).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'test-download-button')))
                            download_btn.click()
                        except TimeoutException:
                            print("Thread {}. TimeoutException 5 for file {} ".format(thread, num))
                            browser.refresh()
                            download_btn = WebDriverWait(browser, 50).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'test-download-button')))
                            download_btn.click()
            except StaleElementReferenceException:
                print("Thread {}. StaleElementReferenceException for file {} ".format(thread, num))
                browser.refresh()
                download_btn = WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'test-download-button')))
                download_btn.click()
        except StaleElementReferenceException:
            print("Thread {}. StaleElementReferenceException for file {} ".format(thread, num))
            browser.refresh()
            download_btn = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'test-download-button')))
            download_btn.click()
        except Exception as e:
            print("Thread {}. Common exception for file {} ".format(thread, num))
            browser.refresh()
            download_btn = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'test-download-button')))
            download_btn.click()

        print("Thread {}. File {} downloaded. Files left {}".format(thread, num, firstInd+len(links)-num))

def assignFileNameToEntityID(browser, thread):
    global page_counter
    tableRows = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, ' css-14pzyw')))
    fileName = tableRows[1].find_elements_by_tag_name("td")[0].get_attribute("innerHTML")

    downstream = WebDriverWait(browser, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'test-downstream-analyses')))
    # while(downstream[0].find_elements_by_tag_name("h2")[0].get_attribute("innerHTML") == 'No Downstream Analysis files found.'): # if no files found refresh page
    #     browser.refresh()
    #     time.sleep(5)
    #     downstream = WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'test-downstream-analyses')))
    #     print("Case didn't load: " + downstream[0].find_elements_by_tag_name("h2")[0].get_attribute("innerHTML"))

    try:
        entityTable = WebDriverWait(browser, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'test-entity-table-wrapper')))
        run = True
        while run:
            if 'TCGA' in entityTable[2].find_elements_by_tag_name("a")[0].get_attribute("innerHTML"):
                entityID = entityTable[2].find_elements_by_tag_name("a")[0].get_attribute("innerHTML") # entityID
                run = False
            else:
                browser.refresh()
                entityTable = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'test-entity-table-wrapper')))
                entityID = entityTable[2].find_elements_by_tag_name("a")[0].get_attribute("innerHTML")  # entityID

    except TimeoutException:
        browser.refresh()
        entityTable = WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'test-entity-table-wrapper')))
    except:
        browser.refresh()
        entityTable = WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'test-entity-table-wrapper')))

    file = "fileWithEntityID" + str(thread) + '.txt'
    f = open(file, 'a')
    f.write(fileName + ":" + entityID + '\n')
    f.close()
    print(str(page_counter) + ":  " + fileName + ":" + entityID)
    page_counter = page_counter + 1

def assigning(links, firstInd, thread = 1):
    browser = browser_setup()
    for num, link in enumerate(links, start=firstInd):
        try:
            browser.get(link)
            try:
                accept_terms(browser)
            except:
                pass
            assignFileNameToEntityID(browser, thread)
        except:
            print("Thread {}. TimeoutException 1 for file {} ".format(thread, num))
            browser.get(link)
            accept_terms(browser)
            time.sleep(3)
            assignFileNameToEntityID(browser, thread)
        print("Thread {}. File {} downloaded. Files left {}".format(thread, num, firstInd + len(links) - num))

def parallelAssigning(list):
    t = threading.Thread(target=assigning, args=(list[0: 396], 0, 1))
    t1 = threading.Thread(target=assigning, args=(list[397: 793], 397, 2))
    t2 = threading.Thread(target=assigning, args=(list[793:], 793, 3))

    t.start()
    t1.start()
    t2.start()

def downloading(list):
    t = threading.Thread(target=download_from_links, args=(list[0: 396], 0, 1))
    t1 = threading.Thread(target=download_from_links, args=(list[397: 793], 397, 2))
    t2 = threading.Thread(target=download_from_links, args=(list[793:], 793, 3))
    #t3 = threading.Thread(target=download_from_links, args=(list[894:], 894, 4))

    t.start()
    t1.start()
    t2.start()
    #t3.start()

def unzip_files(list):
    '''First unzipin'''
    for file in list:
        if (file.endswith("tar.gz")):
            tar = tarfile.open(file, "r:gz")
            tar.extractall(path='/Users/frozmannik/Desktop/LUAD data/extracted')
            tar.close()
        elif (file.endswith("tar")):
            tar = tarfile.open(file, "r:")
            tar.extractall(path='/Users/frozmannik/Desktop/LUAD data/extracted')
            tar.close()
    print("All files are unziped")

def save_txt(folders, path):
    '''second unzip'''
    '''unzip files and save them in folder'''
    for folder in folders:
        if folder == '.DS_Store':
            print("DS STORE")
        else:
            for file in os.listdir(folder):
                    if file.endswith(".gz"):
                        #i = i+1
                        content = gzip.open(folder + "/" +file)
                        data = content.read()
                        with open(os.path.join(path, file[:-3]), "wb") as f: # write bytes to file
                            f.write(data)
    print("All files are saved in {}".format(path))

def save_links_without_page(list):
    with open('links_without_page.txt', 'w') as f:
        for item in list:
            f.write("%s\n" % item)

if __name__ == '__main__':
    items_links = []

    urlLUSC = 'https://portal.gdc.cancer.gov/repository?facetTab=files&files_size=100&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%5B%22TCGA-LUSC%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22files.data_category%22%2C%22value%22%3A%5B%22Transcriptome%20Profiling%22%5D%7D%7D%5D%7D&searchTableTab=files'
    urlLUSCLast = 'https://portal.gdc.cancer.gov/query?files_offset=2800&files_size=100&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%5B%22TCGA-LUAD%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22files.data_category%22%2C%22value%22%3A%5B%22Transcriptome%20Profiling%22%5D%7D%7D%5D%7D%5D%7D&query=cases.project.project_id%20in%20%5BTCGA-LUAD%5D%20and%20files.data_category%20in%20%5B%22Transcriptome%20Profiling%22%5D%20&searchTableTab=files'

    urlLUADLast ='https://portal.gdc.cancer.gov/query?files_offset=2900&files_size=100&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%5B%22TCGA-LUAD%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22files.data_category%22%2C%22value%22%3A%5B%22Transcriptome%20Profiling%22%5D%7D%7D%5D%7D%5D%7D&query=cases.project.project_id%20in%20%5BTCGA-LUAD%5D%20and%20files.data_category%20in%20%5B%22Transcriptome%20Profiling%22%5D%20&searchTableTab=files'
    urlLUAD = 'https://portal.gdc.cancer.gov/query?files_size=100&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%5B%22TCGA-LUAD%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22files.data_category%22%2C%22value%22%3A%5B%22Transcriptome%20Profiling%22%5D%7D%7D%5D%7D%5D%7D&query=cases.project.project_id%20in%20%5BTCGA-LUAD%5D%20and%20files.data_category%20in%20%5B%22Transcriptome%20Profiling%22%5D%20&searchTableTab=files'

    #first_open_url(urlLUSC)
    #links = file_to_list('/Users/frozmannik/PycharmProjects/biologyScrape/links_without_page.txt')

    files = file_to_list("/Users/frozmannik/PycharmProjects/biologyScrape/mergedLUSC.txt")
   # parallelAssigning(links)
    #assignFileNameToEntityID('https://portal.gdc.cancer.gov/files/a53757ce-a89e-47a3-bd07-0c996f323499')
    #first_open_url(urlLUADLast)
   # os.chdir('/Users/frozmannik/Desktop/LUAD data/extracted')
    #unzip_files(os.listdir('/Users/frozmannik/Desktop/LUAD data'))
   # path = '/Users/frozmannik/Desktop/LUAD data/extracted/files'
    #downloading(list)
    #print( os.listdir('/Users/frozmannik/Desktop/data/extracted'))
    #save_txt(os.listdir('/Users/frozmannik/Desktop/LUAD data/extracted'), path)
   # save_links_without_page(items_links)

    #print(len(os.listdir('/Users/frozmannik/Desktop/LUAD data')))
    dic = {}
    path = '/Users/frozmannik/Desktop/finaltxtLUSC/'
    os.chdir('/Users/frozmannik/Desktop/finaltxtLUSC')  # set working directory
    for file in files:
        oldName, newName = file.split(":")[0],file.split(":")[1]
        #print(oldName +" : " + newName)
        if "-UQ" in oldName:
            newName = newName + "-UQ"
        try:
            os.rename(path+oldName[:-3],path+newName+".txt")
        except FileNotFoundError:
            print("file not found")


   # print(os.listdir())
    print("end of execution")
    #print(os.listdir('/Users/frozmannik/Desktop/LUAD data'))


