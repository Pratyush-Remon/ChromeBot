from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option("detach", True)

def get_links():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://myip.ms/browse/sites/1/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/2/asc/1/")
    table_elem = driver.find_element(By.ID, "sites_tbl")
    link_elems = table_elem.find_elements(By.TAG_NAME, "a")
    links = [elem.get_attribute("href") for elem in link_elems if "view/sites" in elem.get_attribute("href")]
    driver.quit()
    return links

def remove_duplicates(links):
    unique_links = []
    for link in links:
        if link not in unique_links:
            unique_links.append(link)
    return unique_links

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
        f.write("\n".join(links))
    return file_name

links = get_links()
unique_links = remove_duplicates(links)
file_name = save_links_to_file(unique_links)
print(f"Links saved to file: {file_name}")
