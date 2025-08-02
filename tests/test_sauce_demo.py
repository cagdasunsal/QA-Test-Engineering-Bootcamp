import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com/"


def login(driver):
    driver.get(URL)
    driver.maximize_window()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")

    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    try:
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Tamam']"))
        ).click()
    except:
        pass

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login(driver):
    login(driver)
    assert "inventory" in driver.current_url



def test_add_to_cart(driver):
    login(driver)
    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Add to cart']"))
    )
    add_button.click()

    badge = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert badge.text == "1"


def test_remove_from_cart(driver):
    login(driver)


    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Add to cart']"))
    )
    add_button.click()


    remove_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Remove']"))
    )
    remove_button.click()





def test_invalid_login(driver):
    driver.get(URL)
    driver.maximize_window()

    driver.find_element(By.ID, "user-name").send_keys("hatalikullanici")
    driver.find_element(By.ID, "password").send_keys("yanlissifre")
    driver.find_element(By.ID, "login-button").click()

    error_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//h3[contains(@data-test,'error')]"))
    )
    assert "Epic sadface" in error_message.text
