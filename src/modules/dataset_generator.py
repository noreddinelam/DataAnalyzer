import os
import requests
from bs4 import BeautifulSoup

GOOGLE_IMAGES_URL = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive"
}

DATASET_FOLDER = "../dataset"


def main():
    if not os.path.exists(DATASET_FOLDER):
        os.mkdir(DATASET_FOLDER)
    download_images()


def download_images():
    DATASET_FOLDER_IMAGES = DATASET_FOLDER + "/images"
    if not os.path.exists(DATASET_FOLDER_IMAGES):
        os.mkdir(DATASET_FOLDER_IMAGES)

    data = input("What are you looking for ? ")
    data = data.strip()
    n_images = int(input("How many images do you want ? "))

    print("Start searching...")

    search_url = GOOGLE_IMAGES_URL + "q=" + data

    response = requests.get(search_url, headers=REQUEST_HEADERS)

    soup = BeautifulSoup(response.content, "html.parser")
    img_results = soup.findAll("img", {"class": "yWs4tf"}, limit=n_images)  # soup.findAll("img", {"class": "yWs4tf"})

    image_links = []
    for result in img_results:
        image_links.append(result["src"])

    print(f"Found {len(image_links)} image" + ('s' if len(image_links) > 1 else ''))

    if len(image_links) > 0:
        DATASET_FOLDER_IMAGES_DATA = DATASET_FOLDER_IMAGES + '/' + data + ('' if data.endswith('s') else 's')
        if not os.path.exists(DATASET_FOLDER_IMAGES_DATA):
            os.mkdir(DATASET_FOLDER_IMAGES_DATA)

        print("Start downloading...")

        for i, image_link in enumerate(image_links):
            response = requests.get(image_link)

            image_name = DATASET_FOLDER_IMAGES_DATA + '/' + str(i + 1) + ".jpg"
            with open(image_name, "wb") as file:
                file.write(response.content)

        print("Done !")


if __name__ == '__main__':
    main()
