from datetime import datetime
import logging
import pandas as pd
import smtplib
import ssl
import sqlite3

# init logging
logging.basicConfig(format='%(asctime)s, %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logbook.log',
                    force=True,
                    level=logging.INFO)


def send_message(message_props):
    with open('emailconf.txt', 'r') as file:
        props = {line.split('=')[0]: line.split('=')[1].replace('\n', '') for line in file}

    message = """
    The price of %s (average %s) is now %s.
    """ % message_props[0:3]

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(props['server'], props['port'], context=context) as server:
        server.login(props['sender'], props['pass'])
        for receiver in props['receivers'].split(','):
            logging.info('Notify, sending message to: {}'.format(receiver))
            server.sendmail(props['sender'], receiver, message)


def check_bargain(db_name, notify):
    db = sqlite3.connect(db_name)
    routes = pd.read_sql('select distinct route from routes', db)

    info = {
        'current_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'routes': []
    }

    for route in routes['route']:
        query = """
        select price 
        from routes 
        where route = "%s"
        order by search_date desc
        """ % (route,)

        df = pd.read_sql(query, db)

        route_info = (
            route,
            round(df['price'].astype(float).mean(), 2),
            df['price'].values[0],
            True if float(df['price'].values[0]) < df['price'].astype(float).mean() * 0.90 else False
        )

        info['routes'].append(route_info)
        if notify and route_info[3]:
            send_message(route_info)

    return info
