import pytest
from selenium import webdriver
driver = webdriver.Chrome()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('Downloads/chromedriver.exe')
   pytest.driver.set_window_size(1400,1000)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()

def test_all_my_pets():
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('tebalashova@gmail.com')
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'pass')))
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('VasyaLisa')
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   # Список моих питомцев
   pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="all_my_pets"]')))
   statistics = pytest.driver.find_elements(By.CSS_SELECTOR, 'div.task3 div')
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr')))

   pet_cards = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
   amount_of_pets = len(pet_cards)

   amount = statistics[0].text.split('\n')
   amount = amount[1].split(' ')
   amount = int(amount[1])

   print('количество питомцев: ', amount)
   print('количество карточек питомцев: ', amount_of_pets)
   assert amount == amount_of_pets

def test_my_pets_info():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('tebalashova@gmail.com')
   driver.implicitly_wait(5)
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('VasyaLisa')
   driver.implicitly_wait(5)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   driver.implicitly_wait(5)
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   # Список моих питомцев
   pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
   driver.implicitly_wait(5)
   # порверяем фото питомцев
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr img')
   statistics = pytest.driver.find_elements(By.CSS_SELECTOR, 'div.task3 div')
   amount = statistics[0].text.split('\n')
   amount = amount[1].split(' ')
   amount = int(amount[1])

   count = 0
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         count = count + 1
   assert amount == count
   assert amount == len(images)
   assert count > (int(amount// 2))
   print('количество питомцев с фото: ', count)

   # проверяем описания питомцев(есть имя, порода, указан возраст)
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
   pets_descriptions = []
   for i in range(len(descriptions)):
      parts = descriptions[i].text.split(' ')
      pets_descriptions.append(parts[:])
      if len(parts) >= 3:
         assert len(parts[0]) > 0
         assert len(parts[1]) > 0
         assert len(parts[2]) > 0
   assert descriptions[i].text != ''
   print('количество описаний питомцев: ', len(descriptions))
   print('описания питомцев: ', pets_descriptions)

   #проверяем имена питомцев
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
   pets_names = []
   for i in range(len(names)):
      parts = names[i].text.split(' ')
      pets_names.append(parts[0])

   print('количество имен питомцев: ', len(pets_names))
   print('имена питомцев: ', pets_names)
   assert names[i].text != ''

