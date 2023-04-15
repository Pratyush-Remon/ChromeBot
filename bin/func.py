from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
options = Options()
options.add_experimental_option("detach", True)

def init_driver():
        driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
        return driver
    


def get_links(driver,str):
    driver.get(str)
    table_elem = driver.find_element(By.ID, "sites_tbl")
    link_elems = table_elem.find_elements(By.TAG_NAME, "a")
    links = [elem.get_attribute(
        "href") for elem in link_elems if "view/sites" in elem.get_attribute("href")]
    return links


def remove_duplicates(links):   
    unique_links = []
    for link in links:
        if link not in unique_links:
            unique_links.append(link)
    return unique_links


def click_table_button(driver,addr, start,end):
    driver.get(addr)
    button_elem = driver.find_element(
        By.CSS_SELECTOR, f"a[href='#{start}']")
    button_elem.click()
    sleep(4)  # Wait for table to update (adjust time as necessary)
    click_im_human_button(driver)
    sleep(4)
    while (start != end+1):
        sleep(4)
        click_table_button2(driver, start)
        start += 1


def click_table_button2(driver, start):
    button_elem = driver.find_element(By.CSS_SELECTOR, f"a[href='#{start}']")
    links = get_links(addr)
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
    with open(file_name, "w") as f:
        for link in links:
            parts = link.split("/")
            cleaned_link = "/".join([parts[0], "", "", parts[6]])
            part = list(cleaned_link)
            i = 0

            shash_count = 0

            final_link = ""

            length = len(part)
            while (i < length):
                if part[i] == "/":
                    shash_count += 1

                if shash_count == 2:
                    i += 1
                    shash_count += 1

                final_link += part[i]

                i += 1

            f.write(final_link + "\n")
    return file_name


def click_im_human_button(driver):
    im_human_button = driver.find_element(By.ID, "captcha_submit")
    im_human_button.click()


addr = "https://myip.ms/browse/sites/1/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/2/asc/1/#2"
def start(a,b):
    click_table_button(addr,a,b)
