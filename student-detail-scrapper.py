import requests
from selenium import webdriver
import csv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json


options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Fetching url
print("welcome Here you can scrape the Data of student According to class and year choose accordingly for getting the data")
year=int(input("Enter year"))
grade=input("Enter class")
url="https://emis.cehrd.gov.np/login"

# defining api through which data is to be extracted
targeted_apiurl=f"https://emis.cehrd.gov.np/v1/api/student/getAllStudentInformations?organizationId=22910&classId={grade}&year={year}&month=0&disabilityType=null&severityId=null&section=all&userType=0&symbolNumberStudent=false"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(url)
input("press enter if you entered the neccesary thing")

# collecting cookies from website 
web_cookies=driver.get_cookies()
settings = driver.execute_script("return sessionStorage.getItem('cehrdUserSettings');")
# print(settings)

# checking the data type and process accordingly
if type(settings)==dict:
    tokens = settings["authdata"]
elif type(settings)== str:
    tokens = json.loads(settings)["authdata"]
else:
    print(f"the type of settings id: {type(settings)} ")
driver.quit()

# saving cookies for further processing
session=requests.Session()
for cookie in web_cookies:
    session.cookies.set(cookie['name'],cookie['value'])
dashboard_url="https://emis.cehrd.gov.np/home"

# defining headers
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Accept":"application/json, text/plain, */*",
    "Referer":"https://emis.cehrd.gov.np/student-records/student-informations",
    "Authorization":f"Bearer {tokens}",
    "X-Requested-With": "XMLHttpRequest"
}

# Getting data from the api
response=session.get(targeted_apiurl,headers=headers)
data=response.json()
if "data" in data:
    data=data["data"]
print(data)

# cleanin and saving the data in csv file
with open(f"scraped_dataclass{grade}.csv",'w',newline="",encoding='utf-8') as f:
    writer=csv.writer(f)
    writer.writerow(["Name","symbol-no","Gender","Father-Name","Mother-Name","contact-no","Adress","Class","DOB","Caste","District","Municipality_Name","Tole","Ward"])
    for item in data:
        writer.writerow([item.get("fullName",""),
                         item.get("id",""),
                         item.get("gender",""),
                         item.get("fatherName",""),
                         item.get("motherName",""),
                         item.get("guardianContactNumber",""),
                         item.get("address",""),
                         item.get("currentClass",""),
                         item.get("dateOfBirth",""),
                         item.get("caste",""),
                         item.get("permanentDistrictName",),
                         item.get("permanentMunicipalityName",""),
                         item.get("permanentTole",""),
                         item.get("permanentWard","")
                         ])

print(f"Data of class {grade} of year:{year} is scrapped successfully and saved in csv file")