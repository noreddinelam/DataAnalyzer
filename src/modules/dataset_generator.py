import os
import shutil
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

GOOGLE_IMAGES_URL = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"

DATASET_FOLDER = "../dataset"


def main():
    if os.path.exists(DATASET_FOLDER):
        shutil.rmtree(DATASET_FOLDER)

    make_dir(DATASET_FOLDER)
    download_google_images()


def make_dir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


# https://selenium-python.readthedocs.io/getting-started.html
# https://www.geeksforgeeks.org/download-google-image-using-python-and-selenium/
def download_google_images():
    DATASET_FOLDER_IMAGES = DATASET_FOLDER + "/images"
    make_dir(DATASET_FOLDER_IMAGES)

    data = input("What are you looking for ? ")
    n_images = int(input("How many images do you want ? "))

    print("Start searching...")
    tic = time.perf_counter()

    search_url = GOOGLE_IMAGES_URL + "q=" + data

    options = Options()
    options.headless = False

    browser = webdriver.Firefox(options=options)  # or Chrome()

    browser.get(search_url)
    time.sleep(1)

    image_links = get_image_links(browser, n_images)

    print(f"Found {len(image_links)} image" + ('s' if len(image_links) > 1 else ''))

    browser.quit()

    if len(image_links) > 0:
        DATASET_FOLDER_IMAGES_DATA = DATASET_FOLDER_IMAGES + '/' + data + ('' if data.endswith('s') else 's')
        make_dir(DATASET_FOLDER_IMAGES_DATA)

        print("Start downloading...")

        for i, image_link in enumerate(image_links):
            image_name = DATASET_FOLDER_IMAGES_DATA + '/' + str(i + 1) + ".jpg"
            with open(image_name, "wb") as file:
                file.write(requests.get(image_link).content)

    toc = time.perf_counter()
    print(f"Done in {toc - tic:0.4f} seconds !")

# https://www.geeksforgeeks.org/download-google-image-using-python-and-selenium/
def get_image_links(browser, n_images):
    img_results = browser.find_elements(by=By.CLASS_NAME, value="rg_i")

    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)

        new_height = browser.execute_script("return document.body.scrollHeight")

        # click on "Show more results" (if exists)
        try:
            browser.find_element_by_css_selector(".YstHxe input").click()
            time.sleep(3)
        except:
            pass

        i = 0
        for result in img_results:
            image_link = result.get_attribute("src")
            if image_link is not None and image_link.startswith("https"):
                i += 1

        if i >= n_images:
            break

        img_results = browser.find_elements(by=By.CLASS_NAME, value="rg_i")

        # checking if we have reached the bottom of the page
        if new_height == last_height:
            break

        last_height = new_height

    image_links = []
    for result in browser.find_elements(by=By.CLASS_NAME, value="rg_i"):
        image_link = result.get_attribute("src")

        if image_link is not None and len(image_links) < n_images and image_link.startswith("https"):
            image_links.append(image_link)

    return image_links


if __name__ == '__main__':
    main()
