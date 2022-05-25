from selenium import webdriver
import time
import pickle
from selenium.webdriver import ActionChains

# Входные параметры
cash = 0
non_cash = 0
date = 0
url = 'https://ccskna.smartshell.gg/login'
url2 = 'https://ccskna.smartshell.gg/work-shifts'

# опции браузера
options = webdriver.FirefoxOptions()
options.set_preference('general.useragent.override','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0')
options.set_preference('dom.webdriver.enabled', False)
options.headless = True
broweser = webdriver.Firefox (
                            executable_path='/Users/danilzubarev/PycharmProjects/pythonProject/Kassir/geckodriver 2',
                            options = options
                             )
try:
# Вход под логином и поролем
    broweser.get(url = url)
    time.sleep(2)
    login = broweser.find_element(by = 'xpath' , value = '/html/body/div[1]/div[2]/div/div[1]/form/div[1]/label/input')
    login.send_keys('Danil')
    password = broweser.find_element(by='xpath', value = '/html/body/div[1]/div[2]/div/div[1]/form/div[2]/label/input')
    password.send_keys('Danil87')
    buton = broweser.find_element(by='xpath', value = '/html/body/div[1]/div[2]/div/div[1]/form/button').click()
    time.sleep(2)
# Сбор куки
    pickle.dump(broweser.get_cookies(), open('cookies', 'wb'))
    time.sleep(2)

    for cookie in pickle.load(open('cookies', 'rb')):
        broweser.add_cookie(cookie)
# Переход на страницу отчетов по кассе
    time.sleep(3)
    broweser.get(url=url2)
    time.sleep(2)
    buton_shifts = broweser.find_element(by='xpath', value='/html/body/div[1]/div[2]/div/div/main/div/div/div[2]')
    action = ActionChains(broweser)
    action.double_click(buton_shifts).perform()
    time.sleep(5)
# Сбор требуемых данных
    cash = broweser.find_element(by='xpath', value='/html/body/div[2]/div/div/div[2]/div[1]/div[2]/span[1]')
    non_cash = broweser.find_element(by='xpath', value='/html/body/div[2]/div/div/div[2]/div[1]/div[3]/span[1]')
    data = broweser.find_element(by='xpath', value='/html/body/div[2]/div/div/div[2]/div[1]/div[1]/div[4]/div[1]/span')
    cash = int(float(''.join(cash.text[:-2:].split()).replace(',','.'))//1)
    non_cash = int(float(''.join(non_cash.text[:-2:].split()).replace(',','.'))//1)
    date = int(data.text.split('.')[0])
except Exception as ex:
    print(ex)

finally:
    broweser.close()
    broweser.quit()