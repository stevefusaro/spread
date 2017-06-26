import getpass
import pickle
import time

from selenium import webdriver

from constants import DATA_DIR


class Driver(webdriver.Firefox):

    def find_el(self, css_selector):
        return self.find_element_by_css_selector(css_selector)


def get_driver(force_new_cookie=True):
    driver = Driver()
    driver.get('http://www.runyourpool.com/')
    cookie_path = '/'.join([DATA_DIR, 'cookies.pkl'])
    try:
        if force_new_cookie:
            raise IOError
        cookies = pickle.load(open(cookie_path, 'rb'))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except IOError:
        _login(driver)
        pickle.dump(driver.get_cookies(), open(cookie_path, 'wb'))
    return driver


def _login(driver):
    username = input('RunYourPool Username: ')
    password = getpass.getpass('RunYourPool Password: ')

    el = driver.find_element_by_name('username')
    el.send_keys(username)

    el = driver.find_element_by_name('password')
    el.send_keys(password)

    submit = driver.find_element_by_css_selector('button[type=submit]')
    submit.click()
    time.sleep(2)
