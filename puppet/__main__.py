from datetime import datetime
import logging
import os
import pandas as pd
import random
import requests
import sqlite3
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from common import notify
from puppet.names import NameSpace, Wait


class Bot:
    def __init__(self, driver, db_name, link):
        self.driver = driver
        self.db_name = db_name
        self.link = link
        self.props = self.read_link()

    def read_link(self):
        l = self.link.split('?')
        larr = l[0].split('/')
        props = l[1].split('&')
        props = {p.split('=')[0]: p.split('=')[1] for p in props}

        route_dict = {
            'site': larr[2],
            'type': larr[5],  # oneway
            'route': '/'.join([larr[7], larr[9]])
        }
        route_dict.update(props)
        return route_dict

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
            logging.info('Puppet, rejecting cookies')
            sleep(Wait.short)
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div[2]/button').click()
        except:
            pass


if __name__ == '__main__':  
    # init logging
    logging.basicConfig(format='%(asctime)s, %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='logbook.log',
                        force=True,
                        level=logging.INFO)

    # time randomizer & screen on/off
    hold_sec = random.randint(1, 60)
    logging.info('Puppet, sleeping for {} seconds'.format(str(hold_sec/60)))
    sleep(hold_sec)

    # Read links.
    with open('links.txt', 'r') as lines:
        links = [line for line in lines]
        logging.info('Puppet, {} links to fetch'.format(str(len(links))))

    # Check if file contain links.
    if not links:
        logging.error('Puppet, links.txt is empty or does not exist')
        logging.info('Puppet, aborting')
        quit()

    # Check site status.
    code = 0
    try:
        # I have done this particular line to not compromise site I am using.
        response = requests.get('/'.join(links[0].split('/')[0:3]))
        code = response.status_code
    except requests.exceptions.ConnectionError as e:
        logging.info(e)
    finally:
        if code != 200:
            logging.error('Puppet, unable to reach server - code: %s' % code)
            logging.info('Puppet, aborting')
            quit()
        else:
            logging.info('Puppet, target site responding')

    # Starts main scraping if server responded and file contain links.
    if links and code:
        driver = uc.Chrome()
        db_name = 'travels.db'

        for l in links:
            # Variables.
            l_index = links.index(l)
            bot = Bot(driver, db_name, l)
            names_dict = NameSpace.xpath_dict
            results = {}
            logging.info('Puppet, entering site {}/{}'.format(str(l_index + 1), str(len(links))))

            # Get site and close Cookie banner if appears.
            driver.get(l)
            sleep(Wait.long)
            bot.cookies()
            sleep(Wait.extra_long)

            # Scrap.
            results.update({'route': bot.props['route']})
            results.update({'type': bot.props['type']})
            results.update({'departure_date': bot.props['departureDate']})
            results.update({'search_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            for space in names_dict:
                if space in ['to_carrier_xpath', 'from_carrier_xpath']:
                    results.update(bot.scrap_att(names_dict[space], space.replace('_xpath', ''), 'title'))
                else:
                    results.update(bot.scrap_txt(names_dict[space], space.replace('_xpath', '')))

            bot.save_to_db(results)
            logging.info('Puppet, route {} saved'.format(results['route']))

        notify.check_bargain(db_name, True)
