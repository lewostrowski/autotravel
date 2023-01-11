from datetime import datetime
import pandas as pd
import requests
import sqlite3
from time import sleep
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By

from names import NameSpace, Wait


class Bot:
    def __init__(self, driver, db_name):
        self.driver = driver
        self.db_name = db_name

    def scrap_att(self, name_space, key, att):
        # Scrap element's attribute.
        val = 'unknown'
        for path in name_space:
            full = NameSpace.base + path
            try:
                val = self.driver.find_element(By.XPATH, full).get_attribute(att)
                break
            except:
                pass
        return {key: [val]}

    def scrap_txt(self, name_space, key):
        # Scrap element's text.
        val = 'unknown'
        for path in name_space:
            full = NameSpace.base + path
            try:
                val = self.driver.find_element(By.XPATH, full).text
                break
            except:
                pass
        return {key: [val]}

    def save_to_db(self, to_save):
        # Save results to db.
        db = sqlite3.connect(self.db_name)
        pd.DataFrame(to_save).to_sql('routes', db, if_exists='append', index=False)
        db.commit()
        db.close()
        return 1

    def cookies(self):
        try:
            # Click 'more option' and then 'save' on Cookie banner. This will disable most of the cookies.
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[1]').click()
            sleep(Wait.short)
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div[2]/button').click()
        except:
            pass


if __name__ == '__main__':
    # Read links.
    with open('links.txt', 'r') as lines:
        links = [line for line in lines]

    # Check if file contain links.
    if not links:
        print('No links in file.')
        quit()

    # Check site status.
    code = 0
    try:
        # I have done this particular line to not compromise site I am using.
        response = requests.get('/'.join(links[0].split('/')[0:3]))
        code = response.status_code
    except requests.exceptions.ConnectionError as e:
        print(e)
    finally:
        if code != 200:
            print('Unable to reach server with code: %s' % code)
            quit()

    # Starts main scraping if server responded and file contain links.
    if links and code:
        driver = uc.Chrome()
        for l in links:
            # Variables.
            bot = Bot(driver, 'travels.db')
            destination = '/'.join([l.split('/')[7], l.split('/')[-1].split('?')[0]])
            names_dict = NameSpace.xpath_dict
            results = {}

            # Get site and close Cookie banner if appears.
            driver.get(l)
            sleep(Wait.long)
            bot.cookies()
            sleep(Wait.extra_long)

            # Scrap.
            results.update({'route': destination})
            results.update({'search_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            for space in names_dict:
                if space in ['to_carrier_xpath', 'from_carrier_xpath']:
                    results.update(bot.scrap_att(names_dict[space], space.replace('_xpath', ''), 'title'))
                else:
                    results.update(bot.scrap_txt(names_dict[space], space.replace('_xpath', '')))

            bot.save_to_db(results)





