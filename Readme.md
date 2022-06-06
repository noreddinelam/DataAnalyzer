# DataAnalyzer

## To run the project :

- Create a project in pycharm and choose venv environment.

    - ***Add needed librairies :***
        - **Application :**
            - kivy
            - uvicorn
            - aiofiles
            - gi
            - picamera
            - python-multipart
        - **Models :**
            - tenserflow
            - keras
            - matplotlib
            - numpy
            - ceaborn
        - **Scrapping :**
            - Selenium

    - ***Running the application:***
        - Start By running the application backend from the **api/api.py**.
        - Run the application front from the **mobile/main.py**.

      ***Remark*** : The models are already trained and saved in **models**

    - Once the application is running you can choose between 3 models : digits, letters or cat-vs-dog model.

## Scrapping :

- We implemented a scrapping functionnality in the project and to run it you have to **install scrapping modules above**
  and start dataset_generator from **data/dataset_generator.py**. You have to specifiy the number of pictures and what
  you are looking for.
- The result images are in the ressources directory devided into two sections : **training** and **validation**.