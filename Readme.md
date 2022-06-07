# DataAnalyzer

## To run the project :

- Create a project in pycharm and choose venv environment.

    - ***Add needed librairies :***
        - **Application :**
            - kivy
            - uvicorn
            - aiofiles
            - opencv-python
            - python-multipart
        - **Models :**
            - tenserflow
            - keras
            - matplotlib
            - numpy
            - seaborn
            - sklearn
        - **Scrapping :**
            - Selenium
        - **Sounds :**
            - gtts
            - playsound 1.2.2 using ```pip install playsound=1.2.2```
            - google_translate.py

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

## DataSets :

- If you want to use a valid datasets see the link below :

***Cat VS Dog*** : https://github.com/abdellah-idris/catvsdog_dataset

***letters*** : https://github.com/abdellah-idris/letters_dataset

***digits*** : https://github.com/abdellah-idris/digit_data

###Remark : 
**You need to verify the paths specified in the models and change them according to your dataset location.**