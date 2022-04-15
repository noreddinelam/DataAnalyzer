import os
import shutil
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from src.modules.utils import make_dir

from webdriver_manager.firefox import GeckoDriverManager

DATASET_TRAINING_FOLDER = "../resources/cat-or-dog-dataset/cat-or-dog/cats"
DATASET_VALIDATION_FOLDER = "../resources/cat-or-dog-dataset/cat-or-dog-validation/cats"

# TODO : refactor

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


def main():
    data = input("What are you looking for ? ")
    n_images = int(input("How many images do you want ? "))

    start = time.perf_counter()
    start_generator(data, n_images)
    end = time.perf_counter()

    print(f"Done in {end - start:0.4f} seconds !")


def start_generator(data, n_images):
    PEXELS_IMAGES_URL = "https://www.pexels.com/search/"
    PIXABAY_IMAGES_URL = "https://pixabay.com/images/search/"
    GOOGLE_IMAGES_URL = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"

    search_url = PEXELS_IMAGES_URL + data
    pexels_search_images = search_images("Pexels", search_url, n_images)
    pexels_search_images[0].quit()
    pexels_image_links = pexels_search_images[1]
    print(f"Found on Pexels : {len(pexels_image_links)} image" + ('s' if len(pexels_image_links) > 1 else ''))
    image_links = pexels_image_links
    current_n_images = n_images - len(pexels_image_links)

    if len(image_links) < n_images:
        search_url = PIXABAY_IMAGES_URL + data
        pixabay_search_images = search_images("Pixabay", search_url, current_n_images)
        pixabay_search_images[0].quit()
        pixabay_image_links = pixabay_search_images[1]
        print(f"Found on Pixabay : {len(pixabay_image_links)} image" + ('s' if len(pixabay_image_links) > 1 else ''))
        image_links += pixabay_image_links
        current_n_images = current_n_images - len(pixabay_image_links)

        if len(image_links) < n_images:
            search_url = GOOGLE_IMAGES_URL + "q=" + data
            google_search_images = search_images("Google", search_url, current_n_images)
            google_search_images[0].quit()
            google_image_links = google_search_images[1]
            print(f"Found on Google : {len(google_image_links)} image" + ('s' if len(google_image_links) > 1 else ''))
            image_links += google_image_links

    print(f"Found total {len(image_links)} image" + ('s' if len(image_links) > 1 else ''))

    if len(image_links) > 0:
        if os.path.exists(DATASET_TRAINING_FOLDER):
            shutil.rmtree(DATASET_TRAINING_FOLDER)
            make_dir(DATASET_TRAINING_FOLDER)
        border = int(0.8 * len(image_links))
        download_images(image_links[:border], DATASET_TRAINING_FOLDER)
        download_images(image_links[border:], DATASET_VALIDATION_FOLDER)


def search_images(on, search_url, n_images):
    print("Start searching on " + on + "...")

    options = Options()
    options.headless = False

    browser = driver
    browser.maximize_window()
    browser.get(search_url)
    time.sleep(3)

    return [browser, get_image_links(on, browser, n_images)]


def get_image_links(on, browser, n_images):
    last_height = browser.execute_script("return document.body.scrollHeight")
    img_results = []
    image_links = []
    i = 0
    while i < n_images:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)

        new_height = browser.execute_script("return document.body.scrollHeight")

        try:
            className = ""
            if on == "Pixabay":
                className = ".button--2AOTE"
            elif on == "Google":
                className = ".YstHxe input"
            browser.find_element(by=By.CSS_SELECTOR, value=className).click()
            time.sleep(3)
        except:
            pass

        if new_height == last_height:
            break

        last_height = new_height

        className = ""

        if on == "Pexels":
            className = "MediaCard_image__ljFAl"
        elif on == "Pixabay":
            className = "link--h3bPW img"
        elif on == "Google":
            className = "rg_i"

        img_results = browser.find_elements(by=By.CLASS_NAME, value=className)

        for result in img_results:
            image_link = result.get_attribute("src")
            if image_link is not None and image_link.startswith("https"):
                image_links.append(image_link)
                i += 1

            if i >= n_images:
                break

    return image_links


def download_images(image_links, folder):
    print("Start downloading...")
    for i, image_link in enumerate(image_links):
        image_name = folder + '/' + str(i + 1) + ".jpg"
        with open(image_name, "wb") as file:
            file.write(requests.get(image_link).content)


if __name__ == '__main__':
    main()
