import os
import shutil
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from src.utils.utils import make_dir

from webdriver_manager.firefox import GeckoDriverManager

DATASET_TRAINING_FOLDER = "../resources/digits-dataset/digit-training/"
DATASET_VALIDATION_FOLDER = "../resources/digits-dataset/digit-validation/"

# TODO : refactor

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


def main():
    data = input("What are you looking for ? ")
    n_images = int(input("How many images do you want ? "))

    data_training_path = DATASET_TRAINING_FOLDER + data + ('' if data.endswith('s') else 's')
    data_validation_path = DATASET_VALIDATION_FOLDER + data + ('' if data.endswith('s') else 's')

    make_dir(data_training_path)
    make_dir(data_validation_path)

    start = time.perf_counter()
    start_generator(data, n_images, data_training_path, data_validation_path)
    end = time.perf_counter()

    print(f"Done in {end - start:0.4f} seconds !")


def start_generator(data, n_images, data_training_path, data_validation_path):
    PEXELS_IMAGES_URL = "https://www.pexels.com/search/"
    PIXABAY_IMAGES_URL = "https://pixabay.com/images/search/"
    GOOGLE_IMAGES_URL = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q="

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
            search_url = GOOGLE_IMAGES_URL + data
            google_search_images = search_images("Google", search_url, current_n_images)
            google_search_images[0].quit()
            google_image_links = google_search_images[1]
            print(f"Found on Google : {len(google_image_links)} image" + ('s' if len(google_image_links) > 1 else ''))
            image_links += google_image_links

    print(f"Found total {len(image_links)} image" + ('s' if len(image_links) > 1 else ''))

    if len(image_links) > 0:
        if os.path.exists(data_training_path):
            shutil.rmtree(data_training_path)
            make_dir(data_training_path)
        if os.path.exists(data_validation_path):
            shutil.rmtree(data_validation_path)
            make_dir(data_validation_path)
        border = int(0.8 * len(image_links))
        download_images(image_links[:border], data_training_path)
        download_images(image_links[border:], data_validation_path)


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
            browser.find_element_by_css_selector(className).click()
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
            if image_link is not None and image_link.startswith("https") and image_link not in image_links:
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
