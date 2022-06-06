from selenium import webdriver #https://habr.com/ru/post/273089/ про селениум
import time
import pickle
from selenium.webdriver import ActionChains

# Входные параметры
cash = 0
non_cash = 0
date = 0
url = 'https://admin.smartshell.gg/login'
url2 = 'https://admin.smartshell.gg/work-shifts'

# опции браузера
options = webdriver.FirefoxOptions()
options.set_preference('general.useragent.override','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0')
options.set_preference('dom.webdriver.enabled', False)
options.headless = True
broweser = webdriver.Firefox (
                            #executable_path='/Users/danilzubarev/PycharmProjects/pythonProject/Kassir/geckodriver 2',
                            executable_path='C:\\Users\\SkillAdmin\\PycharmProjects\\Kassir\\Kassir\\geckodriver.exe',
                            options = options
                             )
broweser.implicitly_wait(10)
try:
# Вход под логином и поролем
    broweser.get(url = url)
    login = broweser.find_element(by = 'xpath' , value = '/html/body/div[1]/div[2]/div[1]/form/div/div[1]/div/label/input')
    login.send_keys('79098647007')
    password = broweser.find_element(by='xpath', value = '/html/body/div[1]/div[2]/div[1]/form/div/div[2]/div/label/input')
    password.send_keys('Danil87')
    buton = broweser.find_element(by='xpath', value = '/html/body/div[1]/div[2]/div[1]/form/button').click()
# Сбор куки
    pickle.dump(broweser.get_cookies(), open('cookies', 'wb'))
    time.sleep(2)

    for cookie in pickle.load(open('cookies', 'rb')):
        broweser.add_cookie(cookie)
# Переход на страницу отчетов по кассе
    buton = broweser.find_element(by='xpath', value='/html/body/div[1]/div[2]/div[1]/div/div/div/div').click()
    buton = broweser.find_element(by='xpath', value='/html/body/div[1]/div[2]/div[1]/div/button').click()
    time.sleep(5)
    broweser.get(url=url2)
    buton_shifts = broweser.find_element(by='xpath', value='/html/body/div[1]/div[2]/div/main/div/div/div[2]')
    action = ActionChains(broweser)
    action.double_click(buton_shifts).perform()
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