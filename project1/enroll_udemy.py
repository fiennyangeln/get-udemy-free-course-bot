from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project1.items import Course


from config import *

# Initialise Database
engine = create_engine('sqlite:///courses.db')
Session = sessionmaker(bind=engine)
session = Session()


# Page to load should be:
# 1. it should not be already enrolled - .filter(Course.remarks.isnot("enrolled"))
# 2. it should be a 0-dollar discounted price course


# if the total number (count) of this query is zero, it means there are no such courses for us to enroll in.
# else, we proceed with the work process.
if session.query(Course).filter(Course.discounted_price == 0).filter(Course.remarks.isnot("enrolled").count() == 0:
    print("No free course to enroll :[\n")

else:
    UDEMY_FOLDER_PATH = UDEMY_FOLDER_PATH + "chromedriver.exe" # + "chromedriver" for Mac users
    driver = webdriver.Chrome(UDEMY_FOLDER_PATH)
    driver.get("https://www.udemy.com/join/login-popup/")

    # when you assert something, you tell the program to test if the condition is true.
    # check if Udemy is inside the title
    assert "Udemy" in driver.title

    # we find the email field here.
    email_field = driver.find_element_by_id("id_email")
    email_field.clear() # we clear the field just in case
    email_field.send_keys(UDEMY_EMAIL)

    # we find the password field here.
    password_field = driver.find_element_by_id("id_password")
    password_field.clear() # we clear the field just in case
    password_field.send_keys(UDEMY_PASSWORD)

    try:
        #login by enter
        email_field.send_keys(Keys.RETURN)
    except:
        #need except block to be safe in selenium ??
        wait = WebDriverWait(driver, 10)
        home_page = wait.until(EC.url_to_be("https://www.udemy.com/"))

    print("Login done.")

    # Query to load all courses with discounted_price = 0  and remarks != enrolled
    for row in session.query(Course).filter(Course.discounted_price == 0).filter(Course.remarks.isnot("enrolled")):
        checkout_url = row.checkout_url

        try:
            driver.get(checkout_url)
        except:
            WebDriverWait(driver, 10).until(lambda driver: driver.current_url != checkout_url)

        if "/cart/success/" in driver.current_url:
            driver.implicitly_wait(10) # just in case
            # here we wait up to 15 seconds until the webdriver manages to find the Expected Condition of
            # the element with the class name of "success-lead__action" to be clickable
            element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "success-lead__action")))
            print("successfully enrolled!")

            # update db
            row.remarks = "enrolled"
            session.commit()

        elif driver.current_url.endswith("/overview"):
            print("already enrolled. skipping to next...")


            row.remarks = "enrolled"
            session.commit()

        else:
            print("an error has occured. skipping to next...")
    # finally!
    driver.close()
    print("all enrollment completed.\n")
