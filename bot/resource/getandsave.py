from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os




options = Options()
options.add_experimental_option("detach", True)




def init_driver(addr):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(addr)
        sleep(3)
        return driver
    except Exception as e:
        print(f"Error initializing web driver: {str(e)}")
        return None


def get_links(driver):
    try:
        table_elem = driver.find_element(By.ID, "sites_tbl")
        link_elems = table_elem.find_elements(By.TAG_NAME, "a")
        links_text = [elem.text for elem in link_elems
                      if "/" in elem.get_attribute("href")
                      and not any(sub in elem.get_attribute("href") for sub in ["/info", "/view", "/diagram"])
                      and elem.text]
        return links_text
    except Exception as e:
        print(f"Error getting links: {str(e)}")
        return None


def remove_duplicates(links):
    unique_links = []
    for link in links:
        if link not in unique_links:
            unique_links.append(link)
    return unique_links


def click_table_button(driver, addr, start, end):
    n = 1
    try:
        driver.get(addr)
        button_elem = driver.find_element(By.CSS_SELECTOR, f"a[href='#{1}']")
        button_elem.click()
        sleep(4)  # Wait for table to update (adjust time as necessary)
        click_im_human_button(driver)

        while n < start:
            n = clickbigbutton(driver, start, n)

        while start <= end + 1:
            sleep(4)
            click_table_button2(driver, start, addr)
            start += 1
    except Exception as e:
        print(f"Error clicking table button: {str(e)}")


def clickbigbutton(driver, start, n):
    if start - n <= 3:
        n += start - n
        print(n)
        button_elem = driver.find_element(By.CSS_SELECTOR, f"a[href='#{n}']")
        button_elem.click()
        sleep(3)
    else:
        print("tarbooz lal hai")
        n += 4
        print(n)
        button_elem = driver.find_element(By.CSS_SELECTOR, f"a[href='#{n}']")
        button_elem.click()
        sleep(3)
    return n

    





def click_table_button2(driver, start, addr):
    button_elem = driver.find_element(By.CSS_SELECTOR, f"a[href='#{start}']")
    try:
        links = get_links(driver)
        if links is None:
            print("Error getting links")
            return
        unique_links = remove_duplicates(links)
        file_name = save_links_to_file(unique_links)
        if file_name is None:
            print("Error saving links to file")
        else:
            print(f"Links saved to file: {file_name}")
        button_elem.click()
        sleep(4)  # Wait for table to update (adjust time as necessary)
    except Exception as e:
        print(f"Error clicking table button 2: {str(e)}")


def save_links_to_file(links):
    folder_name = "my_links"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    i = 1
    file_name = f"my_links/links({i}).txt"
    while os.path.exists(file_name) or not links:
        if not links:
            return None
        i += 1
        file_name = f"my_links/links({i}).txt"
    try:
        with open(file_name, "w") as f:
            for link in links:
                similarweb_url = f"https://www.similarweb.com/website/{link}/#overview"
                f.write(similarweb_url + "\n")
        return file_name
    except IOError:
        print("Error saving links to file")
        return None


def click_im_human_button(driver):
    try:
        im_human_button = driver.find_element(By.ID, "captcha_submit")
        im_human_button.click()
    except:
        pass



def start(a, b):
    addr = "https://myip.ms/browse/sites/1/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/6/asc/1#sites_tbl_top"
    driver = init_driver(addr)
    click_table_button(driver, addr, a, b)
    driver.quit()