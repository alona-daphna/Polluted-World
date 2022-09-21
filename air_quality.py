import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import consts

def getData(url=consts.URL):
    r=requests.get(url)
    return r.text

def get_url_according_to_city():
    city = input("Enter city to measure air quality : ")

    path_to_chromedriver = "C:\\Users\\97252\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--headless')
    options.add_argument("window-size=1920x1080")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options = options, executable_path=path_to_chromedriver)
    driver.get(consts.URL)
    # wait for the webpage to load
    time.sleep(3)


    # identify search box
    search_box = WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "LocationSearch_input")) 
    # wait for element to load
    time.sleep(3)
    
    # enter search text
    search_box.send_keys(city)

    WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "LocationSearch_input").get_attribute("value") == city)


    time.sleep(3)
    # need to wait befor sending enter key
    search_box.send_keys(Keys.RETURN)

    return driver.current_url
    
def print_quality_index(overall_quality):
    print("Air Quality Index : ", end="")
    if 50 >= overall_quality >= 0:
        print("Good")
        print("Air pollution poses little to no risk.")

    if 100 >= overall_quality >= 51:
        print("Moderate")
        print("May cause breathing discomfort for people with \nprolonged exposure, asthma or heart disease")
    
    if 150 >= overall_quality >= 101:
        print("Unhealthy for Sensitive Groups")
        print("Members of sensitive groups should limit prolonged outdoor exertion.")
    if 200 >= overall_quality >= 151:
        print("Unhealthy")
        print("Everyone may begin to experience health effects.\nmembers of sensitive groups may experience more serious health effects.")
    if 300 >= overall_quality >= 201:
        print("Very Unhealty")
        print("The entire population is more likely to be affected")


def main():
    

    url = get_url_according_to_city()

    data = getData(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find the required details
    # html class inside of which are the values we need
    result =  soup.find_all(class_="DonutChart--innerValue--2rO41 AirQuality--pollutantDialText--3Y7DJ")

    # Filter the data by classes

    # overall air quality
    # returns one instant of that class
    overall_quality = soup.find(class_="DonutChart--innerValue--2rO41 AirQuality--extendedDialText--2AsJa").text

    # individual air pollutent data
    # returns the list of classes
    air_data = soup.find_all(class_="DonutChart--innerValue--2rO41 AirQuality--pollutantDialText--3Y7DJ")
    air_data=[data.text for data in air_data]

    pollutents = ["O3", "NO2", "SO2", "PM2.5", "PM10", "co"]
    print("Air Quality :", overall_quality)
    for p in pollutents:
        print(p, "level :", air_data[pollutents.index(p)])

    print_quality_index(int(overall_quality))


main()
