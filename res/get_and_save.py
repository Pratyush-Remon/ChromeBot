import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
options = Options()
# options.add_experimental_option("detach", True)

def init_driver():
    driver = uc.Chrome(service=Service(), options=options)
    return driver


def get_links(driver):
    table_elem = driver.find_element(By.ID, "sites_tbl")
    sleep(2)
    link_elems = table_elem.find_elements(By.TAG_NAME, "a")
    sleep(2)
    links = [elem.get_attribute("href") for elem in link_elems 
             if "/" in elem.get_attribute("href") 
             and "/info" not in elem.get_attribute("href") 
             and "/view" not in elem.get_attribute("href") 
             and "/diagram" not in elem.get_attribute("href")]
    return links


def remove_duplicates(links):   
    unique_links = []
    for link in links:
        if link not in unique_links:
            unique_links.append(link)
    return unique_links


def click_table_button(driver, addr, start, end):
    driver.get(addr)
    button_elem = driver.find_element(By.CSS_SELECTOR, f"a[href='#{start}']")
    button_elem.click()
    sleep(4)    # Wait for table to update (adjust time as necessary)
    click_im_human_button(driver)
    sleep(4)
    while start <= end+1:
        sleep(4)
        click_table_button2(driver, start, addr)
        start += 1


def click_table_button2(driver, start, addr):
    button_elem = driver.find_element(By.CSS_SELECTOR, f"a[href='#{start}']")
    links = get_links(driver)
    unique_links = remove_duplicates(links)
    file_name = save_links_to_file(unique_links)
    print(f"Links saved to file: {file_name}")
    button_elem.click()
    sleep(4)  # Wait for table to update (adjust time as necessary)


def save_links_to_file(links):
    import os
    folder_name = "my_links"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_name = "my_links/links.txt"
    i = 1
    while os.path.exists(file_name):
        file_name = f"my_links/links({i}).txt"
        i += 1
    try:
        with open(file_name, "w") as f:
            for link in links:
                f.write(link+ "\n")
        return file_name
    except IOError:
        print("Error saving links to file")
        return None



def click_im_human_button(driver):
    im_human_button = driver.find_element(By.ID, "captcha_submit")
    im_human_button.click()


def start(a, b):
    driver = init_driver()
    addr = "https://myip.ms/browse/sites/1/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/2/asc/1/"
    click_table_button(driver, addr, a, b)
    driver.quit()


start(1, 5)
