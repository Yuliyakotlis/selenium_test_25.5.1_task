import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('D:/projects/Python/Selenium/chromedriver.exe')
    pytest.driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    yield
    pytest.driver.quit()


def test_show_all_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('planka555@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('79Besuda79')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.XPATH, '//h1').text == "PetFriends"

    images = pytest.driver.find_elements(By.XPATH, '//img[@class="card-img-top"]')
    names = pytest.driver.find_elements(By.XPATH, '//h5[@class="card-title"]')
    descriptions = pytest.driver.find_elements(By.XPATH, '//p[@class="card-text"]')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_show_my_pets_table():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('your_email')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('your_pass')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.XPATH, '//h1').text == "PetFriends"

    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')

    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.ID, "all_my_pets")))
    table_element = pytest.driver.find_elements(By.XPATH, "//tbody/tr")

    for row in table_element:
        assert row.find_element(By.XPATH, "./th/img[@src]")
        assert row.find_element(By.XPATH, "./td[1]").text != ''
        assert row.find_element(By.XPATH, "./td[2]").text != ''
        assert row.find_element(By.XPATH, "./td[3]").text != ''
