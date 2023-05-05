import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pandas as pd

load_dotenv()
PROXY = os.getenv("PROXY")
proxies = {
    "http": PROXY,
    "https": PROXY
}


def getCourses(pageNumber, category_id):
    url = "https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={}&page_size=60&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&label_id={}&source_page=topic_page&locale=en_US&currency=usd&navigation_locale=en_US&skip_price=true&sos=pl&fl=lbl".format(str(pageNumber), str(category_id))
    print("getting courses for page: " + str(pageNumber))
    response = requests.get(url, proxies=proxies)
    return response.json()

def getAllCourses():
    category_id = 7380
    pageNumber = 1
    results = []

    while True:
        try:
            res = getCourses(pageNumber, category_id)
            if "detail" in res.keys(): #udemy error message
                break 
            results += res["unit"]["items"] 
        except Exception as e:
            print(e)
            break 
        pageNumber += 1
        if pageNumber > 1000:
            break
    
    df = pd.DataFrame(results)
    df.to_csv("udemyCourses.csv", index=False)



if __name__ == "__main__":
    getAllCourses()
