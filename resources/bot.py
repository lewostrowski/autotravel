from time import sleep
from datetime import datetime
from names import NameSpace, Wait
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By

def read_link(link):
    larr = link.split('/')[7:]
    larr_dict = {
        'from': larr[0],
        'to': larr[-1].split('?')[0]
    }
    props = larr[-1].split('?')[-1].split('&')
    props_dict = {p.split('=')[0]: p.split('=')[1] for p in props}
    larr_dict.update(props_dict)
    return larr_dict

def check_info_att(driver, name_space, key, att):
    val = 'unknown'
    for path in name_space:
        full = NameSpace.base + path
        try:
            val = driver.find_element(By.XPATH, full).get_attribute(att)
            break
        except:
            pass
    return {key: val}

def check_info(driver, name_space, key):
    val = 'unknown'
    for path in name_space:
        full = NameSpace.base + path
        try:
            val = driver.find_element(By.XPATH, full).text
            break
        except:
            pass
    return {key: val}

driver = uc.Chrome()
with open('links.txt', 'r') as links:
    for l in links:
        driver.get(l)
        sleep(Wait.long)

        try:
            cookie_options = '/html/body/div[1]/div/div/div/div[2]/div/button[1]'
            driver.find_element(By.XPATH, cookie_options).click()
            sleep(Wait.short)

            cookie_save = '/html/body/div[1]/div/div/div/div[3]/div[2]/button'
            driver.find_element(By.XPATH, cookie_save).click()
        except:
            pass

        sleep(Wait.extra_long)

        results = {}
        results.update(check_info(driver, NameSpace.to_departure_xpath, 'to_departure'))
        results.update(check_info(driver, NameSpace.to_arrival_xpath, 'to_arrival'))
        results.update(check_info(driver, NameSpace.to_direct_xpath, 'to_direct'))
        results.update(check_info(driver, NameSpace.from_departure_xpath, 'from_departure'))
        results.update(check_info(driver, NameSpace.from_arrival_xpath, 'from_arrival'))
        results.update(check_info(driver, NameSpace.from_direct_xpath, 'from_direct'))
        results.update(check_info(driver, NameSpace.price, 'price'))
        results.update(check_info_att(driver, NameSpace.to_carrier_xpath, 'to_carrier', 'title'))
        results.update(check_info_att(driver, NameSpace.from_carrier_xpath, 'from_carrier', 'title'))
        results.update({'search_date': datetime.now().strftime('%Y-%m-%d %H:%M')})
        print(results)


